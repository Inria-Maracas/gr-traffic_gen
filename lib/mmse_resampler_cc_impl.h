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

#ifndef INCLUDED_TRAFFIC_GEN_MMSE_RESAMPLER_CC_IMPL_H
#define INCLUDED_TRAFFIC_GEN_MMSE_RESAMPLER_CC_IMPL_H

#include <traffic_gen/mmse_resampler_cc.h>
#include <gnuradio/filter/mmse_fir_interpolator_cc.h>
namespace gr {
  namespace traffic_gen {

    class mmse_resampler_cc_impl : public mmse_resampler_cc
    {
     private:
       double d_mu;
       double d_mu_inc;
       gr::filter::mmse_fir_interpolator_cc* d_resamp;
       std::string m_tag_name;
       int packet_sample_count;
       int packet_length;

     public:
      mmse_resampler_cc_impl(float phase_shift, float resamp_ratio, std::string tag_name);
      ~mmse_resampler_cc_impl();

      void handle_msg(pmt::pmt_t msg);

      void forecast(int noutput_items, gr_vector_int& ninput_items_required);
      int general_work(int noutput_items,
                       gr_vector_int& ninput_items,
                       gr_vector_const_void_star& input_items,
                       gr_vector_void_star& output_items);

      float mu() const;
      float resamp_ratio() const;
      void set_mu(float mu);
      void set_resamp_ratio(float resamp_ratio);

    };

  } // namespace traffic_gen
} // namespace gr

#endif /* INCLUDED_TRAFFIC_GEN_MMSE_RESAMPLER_CC_IMPL_H */
