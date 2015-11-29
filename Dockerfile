FROM andrewosh/binder-base

MAINTAINER Jeffrey Kantor <Kantor.1@nd.edu>

USER root

RUN apt-get update
RUN apt-get install -y glpk-utils
RUN apt-get install -y liblapack-dev
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

USER main

# Install python libraries

RUN pip install ipywidgets
RUN pip install simpy
RUN pip install cvxopt
RUN pip install cvxpy
RUN pip install networkx
