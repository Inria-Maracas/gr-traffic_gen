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

#ifndef INCLUDED_TRAFFIC_GEN_MARGINCUT_IMPL_H
#define INCLUDED_TRAFFIC_GEN_MARGINCUT_IMPL_H

#include <traffic_gen/margincut.h>

namespace gr {
  namespace traffic_gen {

    class margincut_impl : public margincut
    {
     private:
      int m_head_margin;
      int m_end_margin;
      std::string m_tag_name;
      bool m_zero_fill;
      int m_length_packet;
      int m_index_packet;


     public:
      margincut_impl(int head_margin, int end_margin, std::string tag_name, bool zero_fill);
      ~margincut_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace traffic_gen
} // namespace gr

#endif /* INCLUDED_TRAFFIC_GEN_MARGINCUT_IMPL_H */

