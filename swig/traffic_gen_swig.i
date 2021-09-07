/* -*- c++ -*- */

#define TRAFFIC_GEN_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "traffic_gen_swig_doc.i"

%{
#include "traffic_gen/mmse_resampler_cc.h"
#include "traffic_gen/insert_burst.h"
#include "traffic_gen/margincut.h"
#include "traffic_gen/gate.h"
#include "traffic_gen/add.h"
%}

%include "traffic_gen/mmse_resampler_cc.h"
GR_SWIG_BLOCK_MAGIC2(traffic_gen, mmse_resampler_cc);
%include "traffic_gen/insert_burst.h"
GR_SWIG_BLOCK_MAGIC2(traffic_gen, insert_burst);
%include "traffic_gen/margincut.h"
GR_SWIG_BLOCK_MAGIC2(traffic_gen, margincut);

%include "traffic_gen/gate.h"
GR_SWIG_BLOCK_MAGIC2(traffic_gen, gate);
%include "traffic_gen/add.h"
GR_SWIG_BLOCK_MAGIC2(traffic_gen, add);
