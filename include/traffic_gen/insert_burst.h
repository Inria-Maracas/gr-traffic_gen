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

#ifndef INCLUDED_TRAFFIC_GEN_INSERT_BURST_H
#define INCLUDED_TRAFFIC_GEN_INSERT_BURST_H

#include <traffic_gen/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace traffic_gen {

    /*!
     * \brief <+description of block+>
     * \ingroup traffic_gen
     *
     */
    class TRAFFIC_GEN_API insert_burst : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<insert_burst> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of traffic_gen::insert_burst.
       *
       * To avoid accidental use of raw pointers, traffic_gen::insert_burst's
       * constructor is in a private implementation
       * class. traffic_gen::insert_burst::make is the public interface for
       * creating new instances.
       */
      static sptr make(std::string tag_name, int end_margin, bool zero_fill);
    };

  } // namespace traffic_gen
} // namespace gr

#endif /* INCLUDED_TRAFFIC_GEN_INSERT_BURST_H */

