import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome import pins
from esphome.core import CORE
from esphome.const import (
    CONF_ID,
    CONF_PIN,
)

CODEOWNERS = ["@iamjoetaylor"]

CONF_DESTINATION = "destination"
CONF_OPCODE = "opcode"
CONF_PHYSICAL_ADDRESS = "physical_address"
CONF_PROMISCUOUS_MODE = "promiscuous_mode"
PIXIES_X = "pixies_x"
PIXIES_Y = "pixies_y"
SETUP_LAMBDA = "setup_lambda"
LOOP_LAMBDA = "loop_lambda"

def validate_raw_data(value):
    if isinstance(value, list):
        return cv.Schema([cv.hex_uint8_t])(value)
    raise cv.Invalid("data must be a list of bytes")


pixie_chroma_ns = cg.esphome_ns.namespace("pixie_chroma")
PixieChromaComponent = pixie_chroma_ns.class_("PixieChromaComponent", cg.Component)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            # cv.Required(CONF_ID): cv.string("asdf"),
            cv.GenerateID(): cv.declare_id(PixieChromaComponent),
            cv.Required(CONF_PIN): pins.internal_gpio_output_pin_schema,
            cv.Optional(PIXIES_X, default=1): cv.int_range(min=1, max=8),
            cv.Optional(PIXIES_Y, default=1): cv.int_range(min=1, max=8),
            cv.Optional(SETUP_LAMBDA): cv.lambda_,
            cv.Optional(LOOP_LAMBDA): cv.lambda_,
        }
    ).extend(cv.COMPONENT_SCHEMA),
    cv.only_with_arduino,
)

async def to_code(config):
    rhs = PixieChromaComponent.new()

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    # https://github.com/connornishijima/Pixie_Chroma/blob/main/library.properties
    cg.add_library("Ticker", None)
    cg.add_library("fastled/FastLED", "3.3.2")
    cg.add_library("connornishijima/Pixie_Chroma", "1.0.4")
    pin = await cg.gpio_pin_expression(config[CONF_PIN])

    cg.add(var.begin(config[CONF_PIN]["number"], config[PIXIES_X], config[PIXIES_Y]))

    if SETUP_LAMBDA in config:
        begin_lambda = await cg.process_lambda(
            config[SETUP_LAMBDA], [], return_type=cg.void
        )
        cg.add(var.set_begin_lambda(begin_lambda))

    if LOOP_LAMBDA in config:
        loop_lambda = await cg.process_lambda(
            config[LOOP_LAMBDA], [], return_type=cg.void
        )
        cg.add(var.set_loop_lambda(loop_lambda))

    cg.add(var.beginLambda())
