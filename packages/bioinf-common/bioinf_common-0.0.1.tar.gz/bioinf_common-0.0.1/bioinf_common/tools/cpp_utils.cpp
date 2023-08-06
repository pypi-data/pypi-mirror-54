#include <iostream>

#include <pybind11/pybind11.h>

#include "cpp_utils.hpp"
#include "type_converters.hpp"

namespace py = pybind11;


Graph::Graph() {
    // needed for pybind11 C++ <-> Python conversions
}


Graph::Graph(const Graph& graph) {
    this->m_nodes = graph.m_nodes;
    this->m_is_directed = graph.m_is_directed;
    this->m_adjacency_matrix = graph.m_adjacency_matrix;
}


Graph::Graph(
    std::vector<std::string> nodes, std::vector<std::tuple<std::string, std::string>> edges,
    bool is_directed
) {
    this->m_nodes = nodes;
    this->m_is_directed = is_directed;

    // construct adjacency matrix
    int N = this->m_nodes.size();
    this->m_adjacency_matrix = arma::Mat<int>(N, N, arma::fill::zeros);

    for(auto const& e : edges) {
        int pos_i = getNodeIndex(std::get<0>(e));
        int pos_j = getNodeIndex(std::get<1>(e));

        this->m_adjacency_matrix(pos_i, pos_j) = 1;
    }
}


int Graph::getNodeIndex(std::string node) const {
    auto begin = this->m_nodes.begin();
    auto end = this->m_nodes.end();

    return std::distance(begin, std::find(begin, end, node));
}


std::vector<std::string> Graph::getNeighbors(std::string node) const {
    std::vector<std::string> neighs;

    int idx = getNodeIndex(node);
    const arma::subview<int> vec = this->m_adjacency_matrix.row(idx);

    for (std::size_t i = 0; i < vec.n_elem; ++i) {
        if (vec[i] == 1) {
            neighs.push_back(this->m_nodes[i]);
        }
    }

    return neighs;
}


std::vector<std::string> Graph::getNodes() const {
    return this->m_nodes;
}


std::vector<std::tuple<std::string, std::string>> Graph::getEdges() const {
    std::vector<std::tuple<std::string, std::string>> edges;
    for (std::size_t i = 0; i < m_adjacency_matrix.n_rows; ++i) {
        for (std::size_t j = 0; j < m_adjacency_matrix.n_cols; ++j) {
            if (m_adjacency_matrix(i, j) != 0) {
                // TODO: consider edge weights
                edges.push_back(std::make_tuple(
                    this->m_nodes[i],
                    this->m_nodes[j]
                ));
            }
        }
    }
    return edges;
}


bool Graph::isDirected() const {
    return this->m_is_directed;
}


std::ostream& operator<< (std::ostream& out, Graph const& graph) {
    out
        << "Adjacency matrix:" << std::endl
        << arma::Mat<int>(graph.m_adjacency_matrix);

    out << "Nodes: ";
    for (auto n : graph.m_nodes) {
        out << "\"" << n << "\" ";
    }
    out << std::endl;

    return out;
}


Graph graph_identity(Graph graph) {
    std::cout << graph << std::endl;
    return graph;
}


PYBIND11_MODULE(cpp_utils, m) {
    // py::class_<Graph>(m, "Graph")
    //     .def(py::init<const Graph&>())
    //     .def(py::init<std::vector<std::string>, std::vector<std::tuple<std::string, std::string>>, bool>())
    //     .def("getNodes", &Graph::getNodes)
    //     .def("getEdges", &Graph::getEdges)
    //     .def("getNeighbors", &Graph::getNeighbors)
    //     .def("isDirected", &Graph::isDirected)
    // ;

    m.def("graph_identity", &graph_identity);
}
