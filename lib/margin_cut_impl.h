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

#ifndef INCLUDED_TRAFFIC_GEN_MARGIN_CUT_IMPL_H
#define INCLUDED_TRAFFIC_GEN_MARGIN_CUT_IMPL_H

#include <traffic_gen/margin_cut.h>

namespace gr {
  namespace traffic_gen {

    class margin_cut_impl : public margin_cut
    {
     private:
      int m_head_margin;
      int m_end_margin;
      std::string m_tag_name;
      bool m_zero_fill;

     protected:
      int calculate_output_stream_length(const gr_vector_int &ninput_items);

     public:
      margin_cut_impl(int head_margin, int end_margin, std::string tag_name, bool zero_fill);
      ~margin_cut_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_int &ninput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace traffic_gen
} // namespace gr

#endif /* INCLUDED_TRAFFIC_GEN_MARGIN_CUT_IMPL_H */

