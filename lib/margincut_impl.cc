/* -*- c++ -*- */
/*
 * Copyright 2021 gr-traffic_gen author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "margincut_impl.h"

namespace gr {
  namespace traffic_gen {

    margincut::sptr
    margincut::make(int head_margin, int end_margin, std::string tag_name, bool zero_fill)
    {
      return gnuradio::get_initial_sptr
        (new margincut_impl(head_margin, end_margin, tag_name, zero_fill));
    }


    /*
     * The private constructor
     */
    margincut_impl::margincut_impl(int head_margin, int end_margin, std::string tag_name, bool zero_fill)
      : gr::block("margincut",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      m_head_margin = head_margin;
      m_end_margin = end_margin;
      m_tag_name = tag_name;
      m_zero_fill = zero_fill;

      m_length_packet = 0;
      m_index_packet = 0;

    }

    /*
     * Our virtual destructor.
     */
    margincut_impl::~margincut_impl()
    {
    }

    void
    margincut_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = std::min(noutput_items,(m_length_packet - m_index_packet));
    }

    int
    margincut_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      uint64_t abs_N, end_N;
      std::vector<tag_t> tags;
      std::vector<tag_t>::iterator it;
      uint64_t burst_start_offset = 0;

      // Get tag with input length
      abs_N = nitems_read(0) ;
      end_N = abs_N + ninput_items[0];
      tags.clear();
      get_tags_in_range(tags, 0, abs_N, end_N);   

      for (it = tags.begin(); it != tags.end(); ++it) {
        if (pmt::symbol_to_string(it->key) == m_tag_name){
          
          //std::cout << "Margin cut - length tag at " << pmt::from_uint64(it->offset) << " for " << pmt::to_uint64(it->value) << " samples \n";

          if ( (m_length_packet - m_index_packet) > m_end_margin){
            std::cout << "MARGINCUT : Previous packet not finished";
            burst_start_offset = it->offset - abs_N;
          }
          else if (((m_length_packet - m_index_packet) < m_end_margin) && (m_length_packet != 0))  {
            std::cout << "MARGINCUT : Previous packet not finished - discard " << m_length_packet - m_index_packet << " samples of end margin \n";
            burst_start_offset = it->offset - abs_N;
          }
          
          m_length_packet = pmt::to_uint64(it->value);
          m_index_packet = 0;
        }
      }

      int sample_count = 0;
      int cut_sample_count = 0;

      if (m_zero_fill) {
        for(int i=burst_start_offset; i<ninput_items[0];i++){
          if (m_index_packet < m_length_packet) {

            if ((m_index_packet >= m_head_margin) && (m_index_packet<m_length_packet - m_end_margin)){
              out[i-burst_start_offset] = in[i];
            }
            else{
              out[i-burst_start_offset] = 0;
            }
            m_index_packet += 1;
            sample_count += 1;
          }
        }
      }
      else {
        for(int i=burst_start_offset; i<ninput_items[0];i++){
          if (m_index_packet < m_length_packet) {
            if ((m_index_packet >= m_head_margin) && (m_index_packet<m_length_packet - m_end_margin)){
              out[i - burst_start_offset - cut_sample_count] = in[i];
              sample_count += 1;
            }
            else{
              cut_sample_count +=1;
            }
            m_index_packet += 1;
          }
        }
      }
      consume_each(ninput_items[0]);
      if (m_length_packet == m_index_packet && m_length_packet != 0) {
        //std::cout << "Margin cut - produce : " << sample_count << ", - input length : " << ninput_items[0] << ", Index packet : " << m_index_packet << "/" << m_length_packet << ", Cut packet : " << cut_sample_count << "\n";
        std::cout << "Margin cut - packet (" << m_length_packet << " samples) processed\n";
        m_index_packet = 0;
        m_length_packet = 0;      
      }
      return sample_count;
    }

  } /* namespace traffic_gen */
} /* namespace gr */

