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
#include "gate_impl.h"

namespace gr {
  namespace traffic_gen {

    gate::sptr
    gate::make(int total_number_of_sample)
    {
      return gnuradio::get_initial_sptr
        (new gate_impl(total_number_of_sample));
    }


    /*
     * The private constructor
     */
    gate_impl::gate_impl(int total_number_of_sample)
      : gr::block("gate",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      m_total_number_sample = total_number_of_sample;
      m_index = 0;
      m_generation_ongoing = true;
      set_tag_propagation_policy(TPP_DONT);
    }

    /*
     * Our virtual destructor.
     */
    gate_impl::~gate_impl()
    {
    }

    void
    gate_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    gate_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex* in = (const gr_complex*)input_items[0];
      gr_complex* out = (gr_complex*)output_items[0];
      uint64_t to_copy = 0;


      if (m_generation_ongoing) {

        uint64_t abs_N, end_N;
        std::vector<tag_t> tags;
        std::vector<tag_t>::iterator it;

        // Get tag with input length
        abs_N = nitems_read(0) ;
        end_N = abs_N + ninput_items[0];
        tags.clear();
        get_tags_in_range(tags, 0, abs_N, end_N);   

        for (it = tags.begin(); it != tags.end(); ++it) {
          tag_t tag;
          tag.offset = nitems_written(0);
          tag.key = it->key;
          tag.value = it->value;
          add_item_tag(0, tag);
        }

        
        to_copy = std::min(ninput_items[0], int(m_total_number_sample - m_index));
        memcpy(out, in, to_copy * input_signature()->sizeof_stream_item(0));
        m_index += to_copy;
      
        if (m_index == m_total_number_sample) {
          tag_t tag;
          tag.offset = nitems_written(0) + to_copy -1;
          tag.key = pmt::mp("end");
          tag.value = pmt::mp("now");
          add_item_tag(0, tag);
          std::cout << "Signal generated - " << m_index << " samples saved with SigMF - offset tag : " << tag.offset <<"\n";
          m_generation_ongoing = false;
        }
        else if (m_index > m_total_number_sample) {
          tag_t tag;
          tag.offset = nitems_written(0) + to_copy ;
          tag.key = pmt::mp("end");
          tag.value = pmt::mp("now");
          add_item_tag(0, tag);
          std::cout << "Signal generated BUT LIMIT PASSED - " << m_index << " samples saved with SigMF\n";
          m_generation_ongoing = false;
        }
        
        consume_each (to_copy);
      }      
      return to_copy;
    }

  } /* namespace traffic_gen */
} /* namespace gr */

