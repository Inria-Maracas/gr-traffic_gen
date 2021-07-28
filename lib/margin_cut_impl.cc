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

#include <pmt/pmt.h>
#include <gnuradio/io_signature.h>
#include "margin_cut_impl.h"

namespace gr {
  namespace traffic_gen {

    margin_cut::sptr
    margin_cut::make(int head_margin, int end_margin, std::string tag_name)
    {
      return gnuradio::get_initial_sptr
        (new margin_cut_impl(head_margin, end_margin, tag_name));
    }


    /*
     * The private constructor
     */
    margin_cut_impl::margin_cut_impl(int head_margin, int end_margin, std::string tag_name)
      : gr::tagged_stream_block("margin_cut",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)), tag_name)
    {
      m_head_margin = head_margin;
      m_end_margin = end_margin;
      m_tag_name = tag_name;
    }

    /*
     * Our virtual destructor.
     */
    margin_cut_impl::~margin_cut_impl()
    {
    }

    int
    margin_cut_impl::calculate_output_stream_length(const gr_vector_int &ninput_items)
    {
      return ninput_items[0] - m_head_margin - m_end_margin;
    }

    int
    margin_cut_impl::work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];
      uint64_t abs_N, end_N;
      std::vector<tag_t> tags;
      std::vector<tag_t>::iterator it;

      // Get tag with input length
      set_tag_propagation_policy(TPP_DONT);
      for (size_t i = 0; i < input_items.size(); i++) {
        abs_N = nitems_read(i);
        end_N = abs_N + noutput_items;
        tags.clear();
        get_tags_in_range(tags, 0, abs_N, end_N);
      }

      // Output traffic without head and end margin
      for(int i=0; i<input_items.size();i++){
        if ((i >= m_head_margin) && (i < (input_items.size() - m_end_margin))){
          out[i - m_head_margin];
        }
      }

      // Update tag with traffic length 
      for (it = tags.begin(); it != tags.end(); ++it) {
        tag_t tag;
        tag.offset = nitems_written(0);
        tag.key = it->key;
        tag.value = pmt::from_long(noutput_items);
        add_item_tag(0, tag); 
      }

      return noutput_items;
    }

  } /* namespace traffic_gen */
} /* namespace gr */

