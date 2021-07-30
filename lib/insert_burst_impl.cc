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
    insert_burst::make()
    {
      return gnuradio::get_initial_sptr
        (new insert_burst_impl());
    }


    /*
     * The private constructor
     */
    insert_burst_impl::insert_burst_impl()
      : gr::block("insert_burst",
              gr::io_signature::make(2, 2, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      d_burst=false;
      d_copy_left=0;
      set_tag_propagation_policy(TPP_DONT);
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
      ninput_items_required[0] = noutput_items;
      ninput_items_required[1] = 0;
    }

    int
    insert_burst_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      const gr_complex *in1 = (const gr_complex *) input_items[1];
      gr_complex *out = (gr_complex *) output_items[0];

      // if (ninput_items[1]==0) {
      //   printf("%s\n", "function called with empty in1 buffer");
      // }
      // Get tag with input length
      uint64_t abs_N, end_N;
      std::vector<tag_t> tags;
      std::vector<tag_t>::iterator it;
      abs_N = nitems_read(1);
      end_N = abs_N + ninput_items[1];
      tags.clear();
      get_tags_in_range(tags, 1, abs_N, end_N, pmt::intern("start_pack"));
      // Check burst tags
      uint64_t to_copy = 0;
      uint64_t copy_start = 0;
      for (it = tags.begin(); it != tags.end(); ++it) {
        printf("%s\n", "Seen start of burst");
        d_copy_left = pmt::to_uint64(it->value);
        copy_start = it->offset-abs_N;
        tag_t tag;
        tag.offset = nitems_written(0)+copy_start;
        tag.key = it->key;
        tag.value = it->value;
        add_item_tag(0, tag);
      }


      uint64_t treated_0 = 0;
      uint64_t treated_1 = 0;
      if (d_copy_left>0) {
        // printf("%s %d\n", "Copying input1", d_copy_left);
        to_copy = std::min(ninput_items[1]-copy_start,d_copy_left);
        if (copy_start>ninput_items[0]) {
          printf("%s\n", "Aaaaagh, not enough in0 items");
        }
        treated_0 = to_copy+copy_start;
        treated_1 = to_copy+copy_start;
        memcpy(out, in, copy_start * input_signature()->sizeof_stream_item (0));
        memcpy(out+copy_start, input_items[1]+copy_start, to_copy * input_signature()->sizeof_stream_item (0));
        d_copy_left -= to_copy;

        // Get tag with input length
        abs_N = nitems_read(1)+copy_start;
        end_N = abs_N + to_copy;
        tags.clear();
        get_tags_in_range(tags, 1, abs_N, end_N);
        // Propagate tags from input one to output
        for (it = tags.begin(); it != tags.end(); ++it) {
          tag_t tag;
          tag.offset = nitems_written(0) +copy_start;
          // printf("%d %d\n", it->offset, copy_start);
          tag.key = it->key;
          tag.value = it->value;
          // add_item_tag(0, tag);
        }
      }else{
        // printf("%s\n", "Consuming in0");
        treated_0 = ninput_items[0];
        treated_1 = ninput_items[1];
        memcpy(out, in, ninput_items[0] * input_signature()->sizeof_stream_item (0));
      }
      // abs_N = nitems_read(0);
      // end_N = abs_N + treated_0;
      // tags.clear();
      // get_tags_in_range(tags, 0, abs_N, end_N);
      // // Propagate tags from input zero to output
      // for (it = tags.begin(); it != tags.end(); ++it) {
      //   tag_t tag;
      //   tag.offset = nitems_written(0)+(it->offset-abs_N);
      //   tag.key = it->key;
      //   tag.value = it->value;
      //   add_item_tag(0, tag);
      // }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume(0,treated_0);
      consume(1,treated_1);
      // printf("%s %d %d \n", "Consuming input0 copy left", treated_0, d_copy_left);
      // Tell runtime system how many output items we produced.
      return treated_0;
    }

  } /* namespace traffic_gen */
} /* namespace gr */
