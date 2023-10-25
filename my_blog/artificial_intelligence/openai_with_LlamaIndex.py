#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
try using github as vector database for openai, instead of specific a file path
"""

__author__ = '__L1n__w@tch'

import pickle
import os
import openai
from llama_index.llms import OpenAI
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext
from llama_hub.github_repo import GithubClient, GithubRepositoryReader

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

BASEDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
cp = configparser.ConfigParser()
cp.read(os.path.join(BASEDIR, "deploy_tools", "user_pass.conf"))

download_loader("GithubRepositoryReader")


def get_docs():
    if os.path.exists("docs.pkl"):
        with open("docs.pkl", "rb") as f:
            docs = pickle.load(f)
    else:
        github_client = GithubClient(cp.get("email_info", "github_token"))
        loader = GithubRepositoryReader(
            github_client,
            owner="L1nwatch",
            repo="my_blog_source",
            filter_directories=(["my_blog", "deploy_tools"], GithubRepositoryReader.FilterType.INCLUDE),
            filter_file_extensions=([".py"], GithubRepositoryReader.FilterType.INCLUDE),
            verbose=True,
            concurrent_requests=10,
        )

        docs = loader.load_data(branch="master")
        with open("docs.pkl", "wb") as f:
            pickle.dump(docs, f)

    return docs


def test():
    docs = get_docs()
    openai.api_key = cp.get("email_info", "openai_key")
    # llm = OpenAI(temperature=0.1, model="gpt-4")
    llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
    service_context = ServiceContext.from_defaults(llm=llm)
    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(
        """PLEASE RESPONSE in JSON format. FORMAT EXAMPLE: {"file_path":"","return the whole file content":""}; """
        """Question: I don't want to send the email anymore, please tell me which file need to be changed, and also correct the code and return the whole file content to me"""
    )
    print(response)


if __name__ == "__main__":
    test()
