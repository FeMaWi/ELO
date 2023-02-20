# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:34:15 2023

@author: Feli
"""

from os import mkdir
from base64 import b64encode
from requests import get as download
from github import Github
from github import InputGitTreeElement        

repository = 'ELO-Database'
branch = 'main'

"""Upload the database to Github"""
def uploadDatabase(access, files_to_upload, commit_message):
    g = Github(access)
    repo = g.get_user().get_repo(repository)

    master_ref = repo.get_git_ref('heads/' + branch)
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(files_to_upload):
        if entry.endswith('.fs'):
            with open('content/'+entry,mode='rb') as input_file:
                data = input_file.read()
                data = b64encode(data)
                blob = repo.create_git_blob(data.decode("utf-8"), "base64")
                element = InputGitTreeElement(entry, '100644', type='blob', sha=blob.sha)
        else:
            with open('content/'+entry) as input_file:
                data = input_file.read()
                element = InputGitTreeElement(entry, '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
    
"""Fetch the database filesystem from Github to working directory"""
def downloadDatabase(filestorage_name):
    url = 'https://raw.githubusercontent.com/FeMaWi/' + repository + '/' + branch + '/' + filestorage_name
    req = download(url)
    try:
        mkdir('content')
    except:
        print("Content already exists")
    f = open('content/'+filestorage_name, 'w+b')
    f.write(req.content)
    f.close()
    return