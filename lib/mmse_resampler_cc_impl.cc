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


#include <stdexcept>
#include <gnuradio/io_signature.h>
#include "mmse_resampler_cc_impl.h"

namespace gr {
  namespace traffic_gen {

    mmse_resampler_cc::sptr
    mmse_resampler_cc::make(float phase_shift, float resamp_ratio, std::string tag_name)
    {
      return gnuradio::get_initial_sptr
        (new mmse_resampler_cc_impl(phase_shift, resamp_ratio, tag_name));
    }


    /*
     * The private constructor
     */
    mmse_resampler_cc_impl::mmse_resampler_cc_impl(float phase_shift, float resamp_ratio, std::string tag_name)
      : gr::block("mmse_resampler_cc",
              io_signature::make2(1, 2, sizeof(gr_complex), sizeof(float)),
              io_signature::make(1, 1, sizeof(gr_complex))),
        d_mu(phase_shift),
        d_mu_inc(resamp_ratio),
        d_resamp(new gr::filter::mmse_fir_interpolator_cc())
    {
      if (resamp_ratio <= 0)
          throw std::out_of_range("resampling ratio must be > 0");
      if (phase_shift < 0 || phase_shift > 1)
          throw std::out_of_range("phase shift ratio must be > 0 and < 1");

      set_inverse_relative_rate(d_mu_inc);
      message_port_register_in(pmt::intern("msg_in"));
      set_msg_handler(pmt::intern("msg_in"),
                      [this](pmt::pmt_t msg) { this->handle_msg(msg); });

      set_tag_propagation_policy(TPP_CUSTOM);

      m_tag_name = tag_name;
      packet_sample_count = 0;
      packet_length = 0;
    }

    /*
     * Our virtual destructor.
     */
    mmse_resampler_cc_impl::~mmse_resampler_cc_impl()
    {
      delete d_resamp;
    }

    void mmse_resampler_cc_impl::handle_msg(pmt::pmt_t msg)
    {
        if (!pmt::is_dict(msg))
            return;
        // set resamp_ratio or mu by message dict
        if (pmt::dict_has_key(msg, pmt::intern("resamp_ratio"))) {
            set_resamp_ratio(pmt::to_float(pmt::dict_ref(
                msg, pmt::intern("resamp_ratio"), pmt::from_float(resamp_ratio()))));
        }
        if (pmt::dict_has_key(msg, pmt::intern("mu"))) {
            set_mu(
                pmt::to_float(pmt::dict_ref(msg, pmt::intern("mu"), pmt::from_float(mu()))));
        }
    }

    void
    mmse_resampler_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      unsigned ninputs = ninput_items_required.size();
      for (unsigned i = 0; i < ninputs; i++) {
        ninput_items_required[i] = (int)ceil((noutput_items * d_mu_inc) + d_resamp->ntaps());
      }
    }

    int
    mmse_resampler_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex* in = (const gr_complex*)input_items[0];
      gr_complex* out = (gr_complex*)output_items[0];

      int ii = 0; // input index
      int oo = 0; // output index

      // Get tag with input length
      uint64_t abs_N, end_N;
      std::vector<tag_t> tags;
      tag_t tag_packet_length;
      std::vector<tag_t>::iterator it;
      abs_N = nitems_read(0);
      end_N = abs_N + noutput_items;
      tags.clear();
      get_tags_in_range(tags, 0, abs_N, end_N);

      //std::cout << "Resemp GET tag IN " << abs_N << " | " << end_N  << "\n";
      if (!tags.empty()) {
        for (it = tags.begin(); it != tags.end(); ++it){
          tag_t tag;
          tag.offset = nitems_written(0);
          tag.key = it->key;
          tag.value = it->value;

          if (it->key==pmt::intern(m_tag_name)){
            tag_packet_length = tag;
          } 
          else if (it->key==pmt::intern("resamp_ratio")){
            set_resamp_ratio(pmt::to_float(it->value));
            add_item_tag(0, tag);
          }
          else {
            add_item_tag(0, tag);
          }
        }
        
        int value = 0;
        value = double(pmt::to_uint64(tag_packet_length.value))/ d_mu_inc;
        tag_packet_length.value = pmt::from_uint64(value);
        add_item_tag(0, tag_packet_length);
        packet_sample_count = 0;
        packet_length = value;
      }


      while (oo < noutput_items && ii < ninput_items[0]) {

          out[oo++] = d_resamp->interpolate(&in[ii], static_cast<float>(d_mu));

          double s = d_mu + d_mu_inc;
          double f = floor(s);
          int incr = (int)f;
          d_mu = s - f;
          ii += incr;
          packet_sample_count += 1;
      }

      consume_each(ii);

      if (packet_sample_count == packet_length && packet_length != 0) {
        // std::cout << "Resemp - produce : " << oo << " - input used/buffer : " << ii << "/" << ninput_items[0] << " - packet index : " << packet_sample_count <<  "\n";
        std::cout << "Resamp - packet (" << packet_length << " samples / " << d_mu_inc << " ratio) processed\n";
        packet_sample_count = 0;
        packet_length = 0;
      }
      return oo;
  
    }

    float mmse_resampler_cc_impl::mu() const { return static_cast<float>(d_mu); }

    float mmse_resampler_cc_impl::resamp_ratio() const
    {
        return static_cast<float>(d_mu_inc);
    }

    void mmse_resampler_cc_impl::set_mu(float mu) { d_mu = static_cast<double>(mu); }

    void mmse_resampler_cc_impl::set_resamp_ratio(float resamp_ratio)
    {
        d_mu_inc = static_cast<double>(resamp_ratio);
        set_inverse_relative_rate(d_mu_inc);
    }
  } /* namespace traffic_gen */
} /* namespace gr */
