#ifndef CPP_UTILS_H
#define CPP_UTILS_H

#include <armadillo>


class Graph {
public:
    Graph();
    Graph(const Graph&);
    Graph(std::vector<std::string>, std::vector<std::tuple<std::string, std::string>>, bool);

    std::vector<std::string> getNodes() const;
    int getNodeIndex(std::string) const;
    std::vector<std::string> getNeighbors(std::string) const;
    std::vector<std::tuple<std::string, std::string>> getEdges() const;
    bool isDirected() const;

    // other
    friend std::ostream& operator<< (std::ostream&, Graph const&);
private:
    bool m_is_directed; // only needed for conversion to correct networkx object
    std::vector<std::string> m_nodes;
    arma::Mat<int> m_adjacency_matrix;
};


#endif
