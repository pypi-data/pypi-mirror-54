#include <limits>
#include <chrono>

#include "../tools/cpp_utils.hpp"
#include "../tools/type_converters.hpp"


void get_node_distances(
    std::vector<int>& dist_list,
    const std::vector<std::string>& ns1, const std::vector<std::string>& ns2,
    bool is_inter_cluster,
    const std::map<std::string,
    std::map<std::string, double>>& precomputed_distances
) {
    for (const std::string& n1 : ns1) {
        int min_dist = std::numeric_limits<int>::max();
        for (const std::string& n2 : ns2) {
            if (is_inter_cluster or n1 != n2) {
                int cur_dist = precomputed_distances.at(n1).at(n2);

                if (cur_dist < min_dist) {
                    min_dist = cur_dist;
                }
            }
        }
        dist_list.push_back(min_dist);
    }
}


double get_avg_node_distances(
    const std::vector<std::string>& ns1, const std::vector<std::string>& ns2,
    bool is_inter_cluster,
    const std::map<std::string,
    std::map<std::string, double>>& precomputed_distances
) {
    std::vector<int> dist_list;

    get_node_distances(
        dist_list,
        ns1, ns2, is_inter_cluster, precomputed_distances);
    get_node_distances(
        dist_list,
        ns2, ns1, is_inter_cluster, precomputed_distances);

    if (dist_list.size() > 0) {
        double sum = std::accumulate(dist_list.begin(), dist_list.end(), 0.0);
        double mean = sum / dist_list.size();

        return mean;
    } else {
        return std::numeric_limits<double>::quiet_NaN();
    }
}


double cluster_separation(
    const std::vector<std::string>& ns1, const std::vector<std::string>& ns2,
    const std::map<std::string,
    std::map<std::string, double>>& precomputed_distances
) {
    double inter_clus = get_avg_node_distances(
        ns1, ns2, true, precomputed_distances);
    double intra_clus01 = get_avg_node_distances(
        ns1, ns1, false, precomputed_distances);
    double intra_clus02 = get_avg_node_distances(
        ns2, ns2, false, precomputed_distances);

    return inter_clus - (intra_clus01 + intra_clus02) / 2;
}


std::vector<double> cluster_separation_multiple(
    const std::vector<std::tuple<std::vector<std::string>, std::vector<std::string>>>& nodeset_pairs,
    const std::map<std::string, std::map<std::string, double>>& precomputed_distances
) {
    auto start = std::chrono::high_resolution_clock::now();

    std::vector<double> res;
    for (const auto& cluster_pair : nodeset_pairs) {
        res.push_back(cluster_separation(
            std::get<0>(cluster_pair), std::get<1>(cluster_pair),
            precomputed_distances
        ));
    }

    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "True CS duration: " << elapsed.count() << "s" << std::endl;
    return res;
}


PYBIND11_MODULE(cluster_separation_cpp, m) {
    m.def(
        "cluster_separation_cpp", &cluster_separation,
        py::arg("ns1"), py::arg("ns2"), py::arg("precomputed_distances")
    );

    m.def(
        "cluster_separation_multiple_cpp", &cluster_separation_multiple,
        py::arg("nodeset_pairs"), py::arg("precomputed_distances")
    );
}
