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

#ifndef INCLUDED_TRAFFIC_GEN_INSERT_BURST_IMPL_H
#define INCLUDED_TRAFFIC_GEN_INSERT_BURST_IMPL_H

#include <traffic_gen/insert_burst.h>

namespace gr {
  namespace traffic_gen {

    class insert_burst_impl : public insert_burst
    {
     private:
      bool d_burst;
      uint64_t d_copy_left;
      std::string m_tag_name;
      uint64_t m_packet_length;
      uint64_t m_packet_index;
      uint64_t m_total_index;
      int m_end_margin;
      bool m_zero_fill;

     public:
      insert_burst_impl(std::string tag_name, int end_margin, bool zero_fill);
      ~insert_burst_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace traffic_gen
} // namespace gr

#endif /* INCLUDED_TRAFFIC_GEN_INSERT_BURST_IMPL_H */
