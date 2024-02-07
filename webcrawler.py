from urllib.request import urlopen
from stackqueue import *
import ssl
from urllib.error import *
import time

"""
webcrawler to start at pomona.edu webpage, perform a serch, 
search will utilize to_visit structure to keep track of web pages it has found

"""


def is_valid_institution_url(url): 
    """
    checks if url is schoool (.edu)
    :param url: (str) representing pomona url
    :return: (bool) true if website is institution url
    """
    search_line = ".edu"  # string being searched for (changed institution.edu to .edu)
    for line in url.split():  # makes the line into a list before being iterated through
        return search_line in line  # if search_line is found then it returns true


def is_full_url(url):
    """
    checks if url link is a full link by checking "http://
    :param url: (str) url to be checked if contains http://
    :return: (bool) returns true if it is a full link
    """
    return ("http" in url) and (" " not in url)  # checks for http and space


def get_all_urls(url):
    """
    checks for full links that cna be found in the given url
    :param url: (str) representing url
    :return: (lst) containing full web links that can be found in that page
    """
    valid_urls = []  # empty list to append urls being searched for
    try:
        context = ssl._create_unverified_context()
        reader = urlopen(url, context=context, timeout=2)
        page_texts = reader.read().decode('ISO-8859-1')
        # print(page_texts)

        search_line = 'href="'  # indexing where to begin our search for the url

        begin_index = page_texts.find(search_line)  # assigns the start point of the first url to be searched

        while begin_index != -1:  # as long as the searchline exists the search process for url continues
            begin_index = begin_index + 6  # the search index is reassigned for the remaining urls after the first
            end_index = page_texts.find('"' or "'", begin_index + 1)  # checks for either double or single quotes
            found_url = page_texts[begin_index:end_index]  # asigns the found url from the begin_index to end_index
            if is_full_url(found_url):  # Checks if the found url starts with http and is valid institution url
                valid_urls.append(found_url)  # adds the url into a list

            begin_index = page_texts.find(search_line, end_index)
    except URLError:
        print("ignoring: " + url)  # this error is an exception so ignoring + url is printed
    except HTTPError:
        print("ignoring: " + url)
    return valid_urls  # returns the urls found as the while loop is left


def filter_institution_urls(url):
    """
    checks for .edu urls only
    :param url: (lst) a list containing urls
    :return: (lst) containing institution urls
    """

    new_url = []  # empty list to append urls
    for link in url:  # iterates through the list of urls
        if is_valid_institution_url(link):  # checks if the url belongs to institution
            new_url.append(link)  # appends the url that fits the requirements
    return new_url  # returns the url list that fit the requirement


def crawl_institution(url, to_visit, num):
    """
    uses Stack() or Queue() classes to iterate through the links, identify valid links and returns a list of the valid
    links
    :param url: (str) url to start with
    :param to_visit: (class) BFS or DFS search method
    :param num: (int) maximun number of links to be obtained
    :return: (list) of strings, the valid urls collected
    """
    visited = []  # an empty list to aappend the colleceted urls
    my_set = set()  # empty set
    sourced_urls = get_all_urls(url)  # creates a list of all urls
    for link in sourced_urls:  # iterates through the list of urls created
        if is_valid_institution_url(link):  # checks if the url belongs to institution
            to_visit.add(link)  # appends the link into the to_visit list which is initially empty for the BFS or DFS

    while not to_visit.is_empty() and len(visited) < num:  # checks that as long as the to_visit list is occupied
        # and the links are less than the maximum number we need, the process of selection continues
        visited_url = to_visit.remove()  # removes the first link from the to_visit list since, has already been tapped
        if visited_url not in my_set:  # checks if the removed link exists in the set
            my_set.add(visited_url)  # if not, it gets added to the set
            visited.append(visited_url)  # the same link is appended to the list called visited,to keep track
            print("crawling" + visited_url)
            institution_links = filter_institution_urls(get_all_urls(visited_url))  # only gets institution related urls in a list
            for link in institution_links:  # iterates through the list of urls
                to_visit.add(link)  # adds the links to the to_visit list

            time.sleep(0.1)  # minimizes time it takes to visit a single url

    return visited  # returns a list of urls that satisfy the named conditions






# Add this at the beginning of your main script or before calling write_institution_urls
institution_name = input("Enter the name of the institution (without .edu): ").strip()
start_url = f"http://{institution_name}.edu"  # Assuming the institution uses http, not https

# Then, you can use start_url as the starting point for your web crawler







def write_institution_urls(start_url, to_visit, max, output_name):
    """
    checks through the given url, identifies the urls that fit the conditions above, prints the urls
    :param start_url: (str) the url to start with
    :param to_visit: (class) BFS or DFS search method
    :param max: (int) the max number of urls needed to be collected
    :param output_name: (str) the output file name
    :return: (str) the urls collected
    """
    output_file = open(output_name, "w")  # opens the file
    link_list = crawl_institution(start_url, to_visit, max)

    for i in link_list:  # iterates through the list of urls
        output_file.write(str(i) + "\n")  # writes the urls in the output file
    output_file.close()  # closes the file
