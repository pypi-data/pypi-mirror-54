#include <chrono>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "cpp_utils.hpp"

namespace py = pybind11;


namespace pybind11 { namespace detail {
template<> struct type_caster<Graph> {
public:
    PYBIND11_TYPE_CASTER(Graph, _("Graph"));

    // Python -> C++
    bool load(py::handle src, bool) {
        std::cout << "Python -> C++" << std::endl;
        auto start = std::chrono::high_resolution_clock::now();
        py::object obj = src.cast<py::object>();

        // check if conversion is possible
        if (
            not py::hasattr(obj, "nodes") or
            not py::hasattr(obj, "edges")
        ) {
            return false;
        }

        // add nodes
        auto it = py::iter(obj.attr("nodes")());

        std::vector<std::string> nodes;
        while (it != py::iterator::sentinel()) {
            nodes.push_back((*it).cast<std::string>());
            ++it;
        }

        // add edges
        auto it2 = py::iter(obj.attr("edges")());

        std::vector<std::tuple<std::string, std::string>> edges;
        while (it2 != py::iterator::sentinel()) {
            edges.push_back((*it2).cast<std::tuple<std::string, std::string>>());
            ++it2;
        }

        bool is_directed = obj.attr("is_directed")().cast<bool>();
        if (not is_directed) {
            it2 = py::iter(obj.attr("edges")());
            while (it2 != py::iterator::sentinel()) {
                auto e = (*it2).cast<py::tuple>();
                std::string source = e[0].cast<std::string>();
                std::string target = e[1].cast<std::string>();

                edges.push_back(std::make_tuple(target, source));
                ++it2;
            }
        }

        // store result
        value = Graph(nodes, edges, is_directed);

        auto finish = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = finish - start;

        std::cout << "Graph construction: " << elapsed.count() << "s" << std::endl;

        return true;
    }

    // C++ -> Python
    static py::handle cast(Graph src, py::return_value_policy /* policy */, py::handle /* parent */) {
        py::object g = py::module::import("networkx").attr(
            src.isDirected() ? "DiGraph" : "Graph")();
        g.attr("add_nodes_from")(src.getNodes());
        g.attr("add_edges_from")(src.getEdges());

        return g.release();
    }
};
}}
