FROM andrewosh/binder-base

MAINTAINER Jeffrey Kantor <Kantor.1@nd.edu>

USER root

RUN apt-get update
RUN apt-get install -y glpk-utils

USER main

# Install python libraries

RUN pip install ipywidgets
RUN pip install cvxopt
RUN pip install cvxpy
RUN pip install simply