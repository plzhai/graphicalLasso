# Graphical Lasso
This is a series of realizations of graphical lasso , which is an idea initially from [Sparse inverse covariance estimation with the graphical lasso](http://statweb.stanford.edu/~tibs/ftp/graph.pdf) by Jerome Friedman , Trevor Hastie , and Robert Tibshirani.
Graphical Lasso maximizes likelihood of precision matrix:
<div align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex=|\Theta|^{M&space;/&space;2}&space;\exp&space;\left(-\sum_{m=1}^{M}&space;\frac{1}{2}&space;\mathbf{X}(m)^{T}&space;\Theta&space;\mathbf{X}(m)\right)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?|\Theta|^{M&space;/&space;2}&space;\exp&space;\left(-\sum_{m=1}^{M}&space;\frac{1}{2}&space;\mathbf{X}(m)^{T}&space;\Theta&space;\mathbf{X}(m)\right)" title="|\Theta|^{M / 2} \exp \left(-\sum_{m=1}^{M} \frac{1}{2} \mathbf{X}(m)^{T} \Theta \mathbf{X}(m)\right)" /></a></div>
The objective can be formulated as,
<div align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\max&space;_{\Theta}&space;\log&space;\operatorname{det}&space;\Theta-\operatorname{tr}(\mathbf{S}&space;\Theta)-\rho\|\Theta\|_{1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\max&space;_{\Theta}&space;\log&space;\operatorname{det}&space;\Theta-\operatorname{tr}(\mathbf{S}&space;\Theta)-\rho\|\Theta\|_{1}" title="\max _{\Theta} \log \operatorname{det} \Theta-\operatorname{tr}(\mathbf{S} \Theta)-\rho\|\Theta\|_{1}" /></a></div>


Before that, Estimation of Precision is based on neighborhood regression, which failed to consider overall information,
<div align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\min_{\beta_{1}}||X_1-X_{\beta_{2:end}}||^{2}&plus;\lambda||\beta_{1}||_{1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\min_{\beta_{1}}||X_1-X_{\beta_{2:end}}||^{2}&plus;\lambda||\beta_{1}||_{1}" title="\min_{\beta_{1}}||X_1-X_{\beta_{2:end}}||^{2}+\lambda||\beta_{1}||_{1}" /></a>
</div>
 Here is a (partial) historical overview of sparse precision estimation.
<div align="center">
    <img src="/img/precision_view.PNG">
</div>

the question is often formulated like this: Given N observations <a href="https://www.codecogs.com/eqnedit.php?latex=X_{i}(i&space;=&space;1,2,...,N)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_{i}(i&space;=&space;1,2,...,N)" title="X_{i}(i = 1,2,...,N)" /></a> , with dimension p , covariance <a href="https://www.codecogs.com/eqnedit.php?latex=\sum" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum" title="\sum" /></a> , how to model the relationship of the p features ? or in more graphcial model terms , how to pin down the edges among the p vertices?

This problem is very practically significant. Say if the price of cement increases, should the price of bricks really increase too, even if there covariance is positive? Probably not, but both might be linked through a series of ETFs like the wages of the labor. The covariance matrix is a victim of causality! Cement and bricks prices have positive covariance because they are both dependent on another set of indices, but have (close to) zero conditional correlation. So conditional independece often matters , which is decided by inverse covariance  matrix.

if the (i,j) entry of the precision matrix C equals to 0 , that is <a href="https://www.codecogs.com/eqnedit.php?latex=C_{ij}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?C_{ij}" title="C_{ij}" /></a> = 0 ,  then the ith and the jth feature are conditional independet given the remain features.

The goal of graphical lasso is to estimate sparse graph, which is often controlled by the inverse coveriance matrix or so-called precision matrix given adequate data and is superiorly fast.

# Laplacian and Precision

A common question is often asked: What is the difference between Graph Laplacian and Precission? The answer is that Laplacian are built on the kernel function and distance, which means that Laplaican considers local manifolds and there is an  positive edge if 2 points are close. However, Precision considers overall structures, which means significantly distant points are also considered in the graph. Say we have 20 points belonging 2 classes, and 10% edges are retained, the graphs are like that,

<div align="center">
    <img src="/img/laplacian.png"   width="400"/>
    <img src="/img/precision.png"   width="400"/>
</div>

The blue lines in the pictures represent positive edges while the gray ones represent negatives. So if precision is used as regularization terms, it has 2 effects: it will make points between one class close and make points in different class diastant.


Edited by [plzhai](https://plzhai.github.io) in 2019/3/24

