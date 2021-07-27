/* -*- c++ -*- */

#define TRAFFIC_GEN_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "traffic_gen_swig_doc.i"

%{
#include "traffic_gen/margin_cut.h"
%}

%include "traffic_gen/margin_cut.h"
GR_SWIG_BLOCK_MAGIC2(traffic_gen, margin_cut);
