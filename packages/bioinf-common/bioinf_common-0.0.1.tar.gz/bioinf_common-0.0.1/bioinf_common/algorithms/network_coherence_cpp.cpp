#include <random>

#include "../tools/cpp_utils.hpp"
#include "../tools/type_converters.hpp"


std::vector<std::string> intersection(
    std::vector<std::string> v1,
    std::vector<std::string> v2
) {
    std::vector<std::string> v3;

    std::sort(v1.begin(), v1.end());
    std::sort(v2.begin(), v2.end());

    std::set_intersection(
        v1.begin(), v1.end(),
        v2.begin(), v2.end(),
        std::back_inserter(v3)
    );

    return v3;
}


double get_fraction_of_nonisolated_nodes(
    const std::vector<std::string>& nodes, const Graph& graph
) {
    double non_isolated_node_num = 0;
    for (std::string n : nodes) {
        std::vector<std::string> neighs = graph.getNeighbors(n);
        int intersection_size = intersection(nodes, neighs).size();

        // don't count intersection with current node
        if(std::find(neighs.begin(), neighs.end(), n) != neighs.end()) {
            intersection_size--;
        }

        if (intersection_size > 0) {
            non_isolated_node_num++;
        }
    }
    return non_isolated_node_num / nodes.size();
}


double compute_network_coherence(
    const Graph& graph,
    const std::vector<std::string>& nodes,
    int reps
) {
    // generate background distribution
    std::vector<std::string> random_nodes(graph.getNodes());

    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> uni(0, random_nodes.size()-1);

    // sample from random nodes
    std::vector<std::string> cur;
    std::vector<double> rand_fractions;
    for (int i = 0; i < reps; ++i) {
        cur.clear();
        for (std::size_t j = 0; j < nodes.size(); ++j) {
            std::string next_node = random_nodes[uni(rng)];
            while (std::find(cur.begin(), cur.end(), next_node) != cur.end()) {
                // next_node in cur
                next_node = random_nodes[uni(rng)];
            }

            cur.push_back(next_node);
        }

        rand_fractions.push_back(get_fraction_of_nonisolated_nodes(cur, graph));
    }

    // do for actual nodes
    double fraction = get_fraction_of_nonisolated_nodes(nodes, graph);

    // compute network coherence
    auto rf = arma::conv_to<arma::rowvec>::from(rand_fractions);
    double nc = (fraction - arma::mean(rf)) / arma::stddev(rf);

    return nc;
}


PYBIND11_MODULE(network_coherence_cpp, m) {
    m.def("get_fraction_of_nonisolated_nodes_cpp", &get_fraction_of_nonisolated_nodes);
    m.def(
        "compute_network_coherence_cpp", &compute_network_coherence,
        py::arg("graph"), py::arg("nodes"), py::arg("reps") = 1000
    );
}
