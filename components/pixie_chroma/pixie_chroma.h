#pragma once

#ifdef USE_ARDUINO

#include "esphome/core/component.h"

#include <Pixie_Chroma.h>

#include <functional>

namespace esphome {
namespace pixie_chroma {

class PixieChromaComponent : public Component, public PixieChroma {
 public:
  PixieChromaComponent(){};

  // Set a lambda for begin
  void set_begin_lambda(std::function<void()> begin_lambda) { this->begin_lambda_ = begin_lambda; }
  // Set a lambda for loop
  void set_loop_lambda(std::function<void()> loop_lambda) { this->loop_lambda_ = loop_lambda; }

  void beginLambda() {
    if (this->begin_lambda_) {
      this->begin_lambda_();
    }
  }

  void loop() override {
    if (this->loop_lambda_) {
      this->loop_lambda_();
    }
  }

 protected:
  std::function<void()> begin_lambda_;
  std::function<void()> loop_lambda_;
};

}  // namespace pixie_chroma
}  // namespace esphome

#endif  // USE_ARDUINO
