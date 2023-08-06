//
// Created by yk on 2019/10/22.
//

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <k4a/k4a.hpp>

#include "include/pyk4a.h"
#include "include/Pixel.h"
#include "include/DepthPixelColorizer.h"
#include "include/StaticImageProperties.h"

namespace py = pybind11;

class pyk4aimage {

public:
    explicit pyk4aimage(k4a::image &image) : _image(std::move(image)) {}

    uint8_t *get_buffer() noexcept {
        return _image.get_buffer();
    }

    const uint8_t *get_buffer() const noexcept {
        return _image.get_buffer();
    }

    auto get_one_size() {
        switch (_image.get_format()) {
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_NV12:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_MJPG:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_YUY2:
                return sizeof(unsigned char);
                break;
            case k4a_image_format_t::K4A_IMAGE_FORMAT_DEPTH16:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_IR16:
                return sizeof(float);
                break;
            default:
                break;
//            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
//            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
        }


    }

private:
    k4a::image _image;
};

class pyk4acalibration {

public:
    pyk4acalibration() = delete;

    explicit pyk4acalibration(const k4a::calibration &c) : _c(c) {}

    k4a::calibration _c;
};

class pyk4atransformation {
public:
    explicit pyk4atransformation(pyk4acalibration &c) {
        _t = k4a::transformation(c._c);
    }

    pyk4atransformation() = default;;

    k4a::transformation _t = nullptr;
};

class pyk4acapture {
public:
    pyk4acapture() = default;

    pyk4acapture(pyk4atransformation &t, k4a_device_configuration_t &config) {
        _trans._t = std::move(t._t);
        _config = config;
    }

    py::array
    get_depth_image(bool colorize = false, bool transform = false) {
        k4a::image img_depth = _cap.get_depth_image();
        k4a::image result_img = img_depth;
        if (transform) {
            result_img = _trans._t.depth_image_to_color_camera(img_depth);
        }
        if (colorize) {
            ColorizeDepthImage(result_img, yk::DepthPixelColorizer::ColorizeBlueToRed,
                               yk::GetDepthModeRange(_config.depth_mode), &depthTextureBuffer);
        }
        int rows = result_img.get_height_pixels();
        int cols = result_img.get_width_pixels();

        return colorize ?
               py::array(
                       py::buffer_info(
                               depthTextureBuffer.data(),
                               sizeof(unsigned char),
                               py::format_descriptor<unsigned char>::format(),
                               3,
                               {rows, cols, 4},
                               {
                                       sizeof(unsigned char) * 4 * cols,
                                       sizeof(unsigned char) * 4,
                                       sizeof(unsigned char)
                               }
                       )
               ) :
               py::array(
                       py::buffer_info(
                               result_img.get_buffer(),
                               sizeof(unsigned short int),
                               py::format_descriptor<unsigned short int>::format(),
                               2,
                               {rows, cols},
                               {
                                       sizeof(unsigned short int) * cols,
                                       sizeof(unsigned short int)
                               }
                       )
               );
    }

    py::array get_ir_image() {
        k4a::image image_ir = _cap.get_ir_image();
        int rows = image_ir.get_height_pixels();
        int cols = image_ir.get_width_pixels();

        return py::array(
                py::buffer_info(
                        image_ir.get_buffer(),
                        sizeof(unsigned short int),
                        py::format_descriptor<unsigned short int>::format(),
                        2,
                        {rows, cols},
                        {
                                sizeof(unsigned short int) * cols,
                                sizeof(unsigned short int)
                        }
                )
        );
    }

    py::array get_color_image(bool transform = false) {
        k4a::image img_color = _cap.get_color_image();
        k4a::image resultImg = img_color;
        if (transform) {
            resultImg = _trans._t.color_image_to_depth_camera(
                    _cap.get_depth_image(), img_color);
        }

        int rows = resultImg.get_height_pixels();
        int cols = resultImg.get_width_pixels();

        return py::array(
                py::buffer_info(
                        resultImg.get_buffer(),
                        sizeof(unsigned char),
                        py::format_descriptor<unsigned char>::format(),
                        3,
                        {rows, cols, 4},
                        {
                                sizeof(unsigned char) * 4 * cols,
                                sizeof(unsigned char) * 4,
                                sizeof(unsigned char)
                        }
                )
        );
    }

    void reset() noexcept {
        _cap.reset();
    }

    float get_temperature_c() const noexcept {
        return _cap.get_temperature_c();
    }

    k4a::capture _cap = nullptr;
    pyk4atransformation _trans;
    k4a_device_configuration_t _config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    std::vector<yk::Pixel> depthTextureBuffer;
};

//class pyk4amanager {
//public:
//    k4a_device_configuration_t _config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
//    k4a::device _device = nullptr;
//    k4a::capture _capture = nullptr;
//    k4a::image image_c = nullptr;
//    k4a::image image_d = nullptr;
//    k4a::transformation _transformation = nullptr;
//    k4a::calibration _calibration;
//
//    std::vector<yk::Pixel> depthTextureBuffer;
//    std::vector<yk::Pixel> irTextureBuffer;
//    uint8_t *colorTextureBuffer;
//
//    pyk4amanager() = default;
//
//    ~pyk4amanager() = default;
//
//    void open(uint32_t index) {
//        _device = k4a::device::open(index);
//    }
//
//    void set_config(k4a_device_configuration_t c) {
//        _config = c;
//        k4a::calibration calib = _device.get_calibration(_config.depth_mode, _config.color_resolution);
//        _transformation = k4a::transformation(calib);
//    }
//
//    void start_cameras() {
//        _device.start_cameras(&_config);
//    }
//
//    k4a::calibration get_calibration() {
//        k4a::calibration calib = _device.get_calibration(_config.depth_mode, _config.color_resolution);
//        return calib;
//    }
//
//    bool get_capture(int timeout) {
//        return _device.get_capture(&_capture);
//    }
//
//    cv::Mat get_color_image() {
//        image_c = _capture.get_color_image();
//        colorTextureBuffer = image_c.get_buffer();
//        colorFrame = cv::Mat(image_c.get_height_pixels(), image_c.get_width_pixels(), CV_8UC4,
//                             colorTextureBuffer);
//        return colorFrame;
//    }
//
//    cv::Mat get_depth_image() {
//        image_d = _capture.get_depth_image();
//        const k4a::image &image_d_t = _transformation.depth_image_to_color_camera(image_d);
//        ColorizeDepthImage(image_d_t, yk::DepthPixelColorizer::ColorizeBlueToRed,
//                           yk::GetDepthModeRange(_config.depth_mode), &depthTextureBuffer);
//        depthFrame = cv::Mat(image_d_t.get_height_pixels(), image_d_t.get_width_pixels(), CV_8UC4,
//                             depthTextureBuffer.data());
//        return depthFrame;
//    }
//};

class pyk4adevice {
public:

    pyk4adevice() = delete;

    explicit pyk4adevice(k4a::device device) {
        _device = std::move(device);
    }

    static uint32_t get_installed_count() {
        return k4a_device_get_installed_count();
    }

    std::string gets() {
        return _device.get_serialnum();
    }


    static pyk4adevice open(uint32_t index) {
        return pyk4adevice(k4a::device::open(index));
    }

    pyk4acalibration get_calibration(k4a_depth_mode_t depth_mode, k4a_color_resolution_t color_resolution) {
        return pyk4acalibration(_device.get_calibration(depth_mode, color_resolution));
    }

    void start_cameras(const k4a_device_configuration_t &configuration) {
        _device.start_cameras(&configuration);
    }

    bool get_capture(pyk4acapture &cap, int timeout) {
        return _device.get_capture(&cap._cap,
                                   std::chrono::milliseconds(timeout));
    }


    k4a::device _device = nullptr;
};


k4a_device_configuration_t config_init() {
    return K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
}

PYBIND11_MODULE(_pyk4a, m) {
//    py::class_<pyk4amanager>(m, "Manager")
//            .def(py::init<>())
//            .def("open", &pyk4amanager::open)
//            .def("get_calibration", &pyk4amanager::get_calibration)
//            .def("start_cameras", &pyk4amanager::start_cameras)
//            .def("get_capture", &pyk4amanager::get_capture)
//            .def("set_config", &pyk4amanager::set_config)
//            .def("get_depth_image", &pyk4amanager::get_depth_image)
//            .def("get_color_image", &pyk4amanager::get_color_image);
    py::class_<pyk4adevice>(m, "Device")
            .def("open", &pyk4adevice::open)
            .def("get_installed_count", &pyk4adevice::get_installed_count)
            .def("get_calibration", &pyk4adevice::get_calibration)
            .def("start_cameras", &pyk4adevice::start_cameras)
            .def("get_capture", &pyk4adevice::get_capture);
    py::class_<pyk4atransformation>(m, "Transformation")
            .def(py::init<pyk4acalibration &>());
    py::class_<pyk4acalibration>(m, "Calibration");
    py::class_<pyk4acapture>(m, "Capture")
            .def(py::init<>())
            .def(py::init<pyk4atransformation &, k4a_device_configuration_t &>())
            .def("get_depth_image", &pyk4acapture::get_depth_image,
                 py::arg("colorize") = false,
                 py::arg("transform") = false)
            .def("get_color_image", &pyk4acapture::get_color_image,
                 py::arg("transform") = false)
            .def("get_ir_image", &pyk4acapture::get_ir_image);
    py::class_<k4a_device_configuration_t>(m, "Configuration")
            .def(py::init(&config_init))
            .def_readwrite("depth_mode", &k4a_device_configuration_t::depth_mode)
            .def_readwrite("color_resolution", &k4a_device_configuration_t::color_resolution)
            .def_readwrite("camera_fps", &k4a_device_configuration_t::camera_fps)
            .def_readwrite("color_format", &k4a_device_configuration_t::color_format)
            .def_readwrite("synchronized_images_only", &k4a_device_configuration_t::synchronized_images_only);
    py::enum_<k4a_depth_mode_t>(m, "depth_mode_t")
            .value("K4A_DEPTH_MODE_OFF", K4A_DEPTH_MODE_OFF)
            .value("K4A_DEPTH_MODE_NFOV_2X2BINNED", K4A_DEPTH_MODE_NFOV_2X2BINNED)
            .value("K4A_DEPTH_MODE_NFOV_UNBINNED", K4A_DEPTH_MODE_NFOV_UNBINNED)
            .value("K4A_DEPTH_MODE_WFOV_2X2BINNED", K4A_DEPTH_MODE_WFOV_2X2BINNED)
            .value("K4A_DEPTH_MODE_WFOV_UNBINNED", K4A_DEPTH_MODE_WFOV_UNBINNED)
            .value("K4A_DEPTH_MODE_PASSIVE_IR", K4A_DEPTH_MODE_PASSIVE_IR)
            .export_values();
    py::enum_<k4a_color_resolution_t>(m, "color_resolution_t")
            .value("K4A_COLOR_RESOLUTION_720P", K4A_COLOR_RESOLUTION_720P)
            .value("K4A_COLOR_RESOLUTION_1080P", K4A_COLOR_RESOLUTION_1080P)
            .value("K4A_COLOR_RESOLUTION_1440P", K4A_COLOR_RESOLUTION_1440P)
            .value("K4A_COLOR_RESOLUTION_1536P", K4A_COLOR_RESOLUTION_1536P)
            .value("K4A_COLOR_RESOLUTION_2160P", K4A_COLOR_RESOLUTION_2160P)
            .value("K4A_COLOR_RESOLUTION_3072P", K4A_COLOR_RESOLUTION_3072P)
            .export_values();
    py::enum_<k4a_fps_t>(m, "fps_t")
            .value("K4A_FRAMES_PER_SECOND_5", K4A_FRAMES_PER_SECOND_5)
            .value("K4A_FRAMES_PER_SECOND_15", K4A_FRAMES_PER_SECOND_15)
            .value("K4A_FRAMES_PER_SECOND_30", K4A_FRAMES_PER_SECOND_30)
            .export_values();
    py::enum_<k4a_image_format_t>(m, "image_format_t")
            .value("K4A_IMAGE_FORMAT_COLOR_MJPG", K4A_IMAGE_FORMAT_COLOR_MJPG)
            .value("K4A_IMAGE_FORMAT_COLOR_NV12", K4A_IMAGE_FORMAT_COLOR_NV12)
            .value("K4A_IMAGE_FORMAT_COLOR_YUY2", K4A_IMAGE_FORMAT_COLOR_YUY2)
            .value("K4A_IMAGE_FORMAT_COLOR_BGRA32", K4A_IMAGE_FORMAT_COLOR_BGRA32)
            .value("K4A_IMAGE_FORMAT_DEPTH16", K4A_IMAGE_FORMAT_DEPTH16)
            .value("K4A_IMAGE_FORMAT_IR16", K4A_IMAGE_FORMAT_IR16)
            .export_values();
    m.attr("K4A_DEVICE_DEFAULT") = K4A_DEVICE_DEFAULT;
    m.def("get_device_count", &k4a_device_get_installed_count);
};