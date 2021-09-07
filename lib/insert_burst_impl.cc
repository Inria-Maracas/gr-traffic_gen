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
#include "insert_burst_impl.h"

namespace gr {
  namespace traffic_gen {

    insert_burst::sptr
    insert_burst::make(std::string tag_name, int end_margin, bool zero_fill)
    {
      return gnuradio::get_initial_sptr
        (new insert_burst_impl(tag_name, end_margin, zero_fill));
    }


    /*
     * The private constructor
     */
    insert_burst_impl::insert_burst_impl(std::string tag_name, int end_margin, bool zero_fill)
      : gr::block("insert_burst",
              gr::io_signature::make(2, 2, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      d_burst=false;
      d_copy_left=0;
      m_tag_name = tag_name;
      m_end_margin = end_margin;
      m_zero_fill = zero_fill;

      m_packet_length = 0;
      m_packet_index = 0;
      m_total_index = 0;
    }

    /*
     * Our virtual destructor.
     */
    insert_burst_impl::~insert_burst_impl()
    {
    }

    void
    insert_burst_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    insert_burst_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in_0_continuous = (const gr_complex *) input_items[0];
      const gr_complex *in_1_burst = (const gr_complex *) input_items[1];
      gr_complex *out = (gr_complex *) output_items[0];

      // if (ninput_items[1] != 0) {
      //   std::cout << "Insert Burst - Input 1 " << ninput_items[1] << " - packet index : " << m_packet_index << "/" << m_packet_length << "\n";
      // }
      uint64_t burst_start_offset = 0;
      uint64_t abs_N, end_N;
      std::vector<tag_t> tags;
      std::vector<tag_t>::iterator it;

      // Get tag with input length
      abs_N = nitems_read(1) ;
      end_N = abs_N + ninput_items[1];
      tags.clear();
      get_tags_in_range(tags, 1, abs_N, end_N);   

      for (it = tags.begin(); it != tags.end(); ++it) {
        if (pmt::symbol_to_string(it->key) == m_tag_name){
                    
          burst_start_offset = it->offset - abs_N;
          //std::cout << "Insert Burst - length tag at " << pmt::from_uint64(it->offset) << " for " << pmt::to_uint64(it->value) << "samples - burst start offset : " << burst_start_offset <<"\n";
          
          tag_t tag;
          tag.offset = nitems_written(0);
          tag.key = it->key;
          tag.value = it->value;
          add_item_tag(0, tag);

          if (m_packet_length != m_packet_index){
            std::cout << "Insert Burst : Previous packet not finished" << m_packet_index << "/" << m_packet_length << "\n";
          }
          
          m_packet_length = pmt::to_uint64(it->value);
          m_packet_index = 0;
        }
        else{
          tag_t tag;
          tag.offset = nitems_written(0);
          tag.key = it->key;
          tag.value = it->value;
          add_item_tag(0, tag);
        }
      }

      d_copy_left = m_packet_length - m_packet_index;
      uint64_t to_copy = std::min(d_copy_left, uint64_t(ninput_items[1] - burst_start_offset));

      if (d_copy_left > 0 && to_copy > 0){
        memcpy(out, &in_1_burst[burst_start_offset], to_copy * input_signature()->sizeof_stream_item(1));
        consume_each(to_copy + burst_start_offset);

        m_packet_index = m_packet_index + to_copy;
        noutput_items = to_copy;

        //std::cout << "Insert Burst - to copy : " << to_copy << " - index : " << m_packet_index << "/" << m_packet_length << " - input : " << ninput_items[1] << "\n";
        if (m_packet_length == m_packet_index && m_packet_length != 0) {
        //std::cout << "Margin cut - produce : " << sample_count << ", - input length : " << ninput_items[0] << ", Index packet : " << m_index_packet << "/" << m_length_packet << ", Cut packet : " << cut_sample_count << "\n";
        std::cout << "Insert burst - packet (" << m_packet_length << " samples) processed\n";
        m_packet_index = 0;
        m_packet_length = 0;      
        }
      }
      else if (d_copy_left == 0){
        memcpy(out, in_0_continuous, ninput_items[0] * input_signature()->sizeof_stream_item(0));
        consume(0, ninput_items[0]);
        consume(1, 0);

        noutput_items = ninput_items[0];
        
      }
      else {
        noutput_items = 0;
        // If missing samples are in end_margin, we discard them
        if (m_zero_fill && (d_copy_left) < m_end_margin) {
          std::cout << "Insert burst - packet (" << m_packet_length << " samples) processed - " << d_copy_left <<" samples in end_margin were discarded\n";
          m_packet_index = m_packet_length;

        } 
        // else if (m_zero_fill && (d_copy_left) >= m_end_margin) {
        //   std::cout << "Insert burst - missing " << d_copy_left << " samples to finish packet";
        // }
      }
      m_total_index += noutput_items;

      return noutput_items;
    }

  } /* namespace traffic_gen */
} /* namespace gr */
