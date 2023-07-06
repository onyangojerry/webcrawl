from urllib.request import urlopen
from stackqueue import *
import ssl
from urllib.error import *
import time

"""
webcrawler to start at pomona.edu webpage, perform a serch, 
search will utilize to_visit structure to keep track of web pages it has found

"""


def is_valid_pomona_url(url):
    """
    checks if url is pomona's (pomona.edu)
    :param url: (str) representing pomona url
    :return: (bool) true if website is Pomona url
    """
    search_line = "pomona.edu"  # string being searched for
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
            if is_full_url(found_url):  # Checks if the found url starts with http and is valid pomona url
                valid_urls.append(found_url)  # adds the url into a list

            begin_index = page_texts.find(search_line, end_index)
    except URLError:
        print("ignoring: " + url)  # this error is an exception so ignoring + url is printed
    except HTTPError:
        print("ignoring: " + url)
    return valid_urls  # returns the urls found as the while loop is left


def filter_pomona_urls(url):
    """
    checks for pomona urls only
    :param url: (lst) a list containing urls
    :return: (lst) containing pomona urls
    """

    new_url = []  # empty list to append pomona urls
    for link in url:  # iterates through the list of urls
        if is_valid_pomona_url(link):  # checks if the url belongs to pomona
            new_url.append(link)  # appends the url that fits the requirements
    return new_url  # returns the url list that fit the requirement


def crawl_pomona(url, to_visit, num):
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
        if is_valid_pomona_url(link):  # checks if the url belongs to pomona
            to_visit.add(link)  # appends the link into the to_visit list which is initially empty for the BFS or DFS

    while not to_visit.is_empty() and len(visited) < num:  # checks that as long as the to_visit list is occupied
        # and the links are less than the maximum number we need, the process of selection continues
        visited_url = to_visit.remove()  # removes the first link from the to_visit list since, has already been tapped
        if visited_url not in my_set:  # checks if the removed link exists in the set
            my_set.add(visited_url)  # if not, it gets added to the set
            visited.append(visited_url)  # the same link is appended to the list called visited,to keep track
            print("crawling" + visited_url)
            pomona_links = filter_pomona_urls(get_all_urls(visited_url))  # only gets pomona related urls in a list
            for link in pomona_links:  # iterates through the list of urls
                to_visit.add(link)  # adds the links to the to_visit list

            time.sleep(0.1)  # minimizes time it takes to visit a single url

    return visited  # returns a list of urls that satisfy the named conditions


def write_pomona_urls(start_url, to_visit, max, output_name):
    """
    checks through the given url, identifies the urls that fit the conditions above, prints the urls
    :param start_url: (str) the url to start with
    :param to_visit: (class) BFS or DFS search method
    :param max: (int) the max number of urls needed to be collected
    :param output_name: (str) the output file name
    :return: (str) the urls collected
    """
    output_file = open(output_name, "w")  # opens the file
    link_list = crawl_pomona(start_url, to_visit, max)

    for i in link_list:  # iterates through the list of urls
        output_file.write(str(i) + "\n")  # writes the urls in the output file
    output_file.close()  # closes the file

"""
Stack()

crawlinghttps://www.pomona.edu/map/?id=523#!m/54434
crawlinghttps://www.pomona.edu/academics/majors/computer-science
crawlinghttps://www.pomona.edu/academics/departments/computer-science/faculty-staff
crawlinghttps://www.pomona.edu/directory/people/corey-leblanc
crawlinghttps://www.pomona.edu/administration/dining/menus/frank
crawlinghttps://www.pomona.edu/map/?id=523#!m/54500
crawlinghttps://catalog.pomona.edu
crawlinghttp://www.pomona.edu/directory/offices-departments
crawlinghttps://www.pomona.edu/administration/writing-center/staff
crawlinghttps://www.pomona.edu/map/?id=523#!m/54445
crawlinghttps://www.pomona.edu/directory/people/jenny-thomas
crawlinghttps://www.pomona.edu/node/1539
crawlinghttps://www.pomona.edu/map/?id=523#!m/54441
crawlinghttps://www.pomona.edu/directory/people/kara-wittman
crawlinghttps://www.pomona.edu/node/1576
crawlinghttps://www.pomona.edu/node/4052
crawlinghttps://www.pomona.edu/administration/writing-center
crawlinghttps://www.pomona.edu/node/3917
crawlinghttps://www.pomona.edu/administration/treasurer/office-treasurer-staff
crawlinghttps://www.pomona.edu/map/?id=523#!m/54413
crawlinghttps://www.pomona.edu/directory/people/lindsey-arias
crawlinghttps://www.pomona.edu/node/1405
crawlinghttps://www.pomona.edu/directory/people/jeff-roth
crawlinghttps://www.pomona.edu/node/6467
crawlinghttps://www.pomona.edu/node/4055
crawlinghttps://www.pomona.edu/administration/treasurer/staff
crawlinghttps://www.pomona.edu/administration/treasurer
crawlinghttps://www.pomona.edu/node/3921
crawlinghttps://www.pomona.edu/academics/departments/theatre/faculty-staff
crawlinghttps://www.pomona.edu/map/?id=523#!m/54819
crawlinghttps://www.pomona.edu/academics/departments/dance
crawlinghttps://www.pomona.edu/map/?id=523#!m/54827
crawlinghttps://www.pomona.edu/academics/majors/dance
crawlinghttps://www.pomona.edu/academics/departments/dance/faculty-staff
crawlinghttps://www.pomona.edu/directory/people/ashanti-l-smalls
crawlinghttps://www.pomona.edu/node/1564
crawlinghttps://www.pomona.edu/directory/people/laurie-cameron
crawlinghttps://www.pomona.edu/node/2088
crawlinghttps://www.pomona.edu/directory/people/anthony-shay
crawlinghttps://www.pomona.edu/node/2089
crawlinghttps://www.pomona.edu/directory/people/jennifer-schulz
crawlinghttps://www.pomona.edu/node/1431
crawlinghttps://www.pomona.edu/directory/people/john-pennington
crawlinghttps://www.pomona.edu/node/1910
crawlinghttps://www.pomona.edu/node/4030
crawlinghttps://www.pomona.edu/academics/departments/dance/prospective-students
crawlinghttps://www.pomona.edu/admissions/apply/how-apply/supplements
crawlinghttps://admissions.pomona.edu/register/information
crawlinghttps://www.pomona.edu/directory/all
crawlinghttps://www.pomona.edu/website-feedback
crawlinghttps://www.pomona.edu/node/3853
crawlinghttps://www.pomona.edu/privacy
crawlinghttps://www.pomona.edu/node/3042
crawlinghttps://www.pomona.edu/support-pomona
crawlinghttp://pomonalegacy.pomona.edu/
crawlinghttps://www.pomona.edu/staff
crawlinghttps://my.pomona.edu/ics
crawlinghttps://www.pomona.edu/digital-accessibility
crawlinghttps://www.pomona.edu/node/4484
crawlinghttps://www.pomona.edu/accessibility/digital
crawlinghttps://www.pomona.edu/directory/people
crawlinghttps://www.pomona.edu/node/3316
crawlinghttps://www.pomona.edu/people
crawlinghttps://www.pomona.edu/administration/division-student-affairs
crawlinghttps://www.pomona.edu/administration/student-affairs/cultural-communities-and-mentor-programs
crawlinghttps://www.pomona.edu/daca
crawlinghttps://www.pomona.edu/administration/career-development/job-internship-search/pcip/summer-experience-international-domestic
crawlinghttps://www.pomona.edu/outcomes
crawlinghttps://www.pomona.edu/administration/institutional-research/information-center
crawlinghttps://tableau.campus.pomona.edu/views/employeedatafromHRsurveysbeta/TotalEmployees?iframeSizedToWindow=true&amp;:embed=y&amp;:display_count=n&amp;:showAppBanner=false&amp;:showVizHome=n&amp;:origin=viz_share_link
crawlinghttps://tableau.campus.pomona.edu/views/employeedatafromHRsurveysbeta/TotalEmployees?iframeSizedToWindow=true&amp;:embed=y&amp;:showAppBanner=false&amp;:display_count=no&amp;:showVizHome=no#1
crawlinghttps://tableau.campus.pomona.edu/views/alumni17/AlumniOutcomes?:embed=y&amp;:showAppBanner=false&amp;:showShareOptions=true&amp;:display_count=no&amp;:showVizHome=no#2
crawlinghttps://tableau.campus.pomona.edu/views/GradratesforIRwebsite/GradRates/69fc1b31-d1d2-4813-bfc3-61b9ffb0b144/5e0ac3b1-d546-44ed-81da-c4c5b583956c?:display_count=n&amp;:showVizHome=n&amp;:origin=viz_share_link
crawlinghttps://tableau.campus.pomona.edu/views/DiversityIndicatorHIPS/HIPS
crawlinghttps://tableau.campus.pomona.edu/views/LightingthePath-ExplorethePlan/Explore?:embed=y&amp;:showAppBanner=false&amp;:showShareOptions=true&amp;:display_count=no&amp;:showVizHome=no#3
crawlinghttps://www.pomona.edu/administration/institutional-research/information-center/historical-enrollment-trends
crawlinghttps://www.pomona.edu/node/5782
crawlinghttps://www.pomona.edu/node/4786
crawlinghttps://www.pomona.edu/administration/institutional-research
crawlinghttps://www.pomona.edu/node/3926
crawlinghttps://www.pomona.edu/after-pomona/alumni-career-stories
crawlinghttps://www.pomona.edu/administration/fellowships
crawlinghttps://www.pomona.edu/administration/career-development/event-calendar
crawlinghttps://www.pomona.edu/node/6093
crawlinghttps://www.pomona.edu/administration/career-development/career-advising-resources/event-calendar
crawlinghttps://www.pomona.edu/news/2022/05/25-recent-pomona-graduates-awarded-fulbrights
crawlinghttps://www.pomona.edu/academics/majors/mathematics
crawlinghttps://www.pomona.edu/academics/departments/mathematics/faculty-staff
crawlinghttps://www.pomona.edu/map/?id=523#!m/54436
crawlinghttps://www.pomona.edu/directory/people/liz-gutierrez
crawlinghttps://www.pomona.edu/node/5312
crawlinghttps://www.pomona.edu/map/?id=523#!m/54435
crawlinghttps://www.pomona.edu/directory/people/sandy-grabiner
crawlinghttps://www.pomona.edu/node/1839
crawlinghttps://www.pomona.edu/directory/people/erica-flapan
crawlinghttps://www.pomona.edu/sites/default/files/person/cv/cv-flapan.pdf
crawlinghttp://pages.pomona.edu/~elf04747/
crawlinghttps://www.pomona.edu/node/1856
crawlinghttps://www.pomona.edu/directory/people/dwight-anderson-williams-ii
crawlinghttps://www.pomona.edu/node/6320

Queue()
crawlinghttps://www.pomona.edu/academics/departments/computer-science/faculty-staff
crawlinghttps://www.pomona.edu/node/4029
crawlinghttps://catalog.pomona.edu
crawlinghttps://www.pomona.edu/administration/dining/menus/frank
crawlinghttps://www.pomona.edu/map/?id=523#!m/54434
crawlinghttps://www.pomona.edu/directory/people/eleanor-birrell
crawlinghttps://www.pomona.edu/directory/people/tzu-yi-chen
crawlinghttps://www.pomona.edu/directory/people/anthony-clark
crawlinghttps://www.pomona.edu/directory/people/joseph-c-osborn
crawlinghttps://www.pomona.edu/directory/people/alexandra-papoutsaki
crawlinghttps://www.pomona.edu/directory/people/yuqing-melanie-wu
crawlinghttps://www.pomona.edu/map/?id=523#!m/54413
crawlinghttps://www.pomona.edu/directory/people/zilong-ye
crawlinghttps://www.pomona.edu/directory/people/thomas-yeh
crawlinghttps://www.pomona.edu/directory/people/kim-b-bruce
crawlinghttps://www.pomona.edu/directory/people/everett-l-bull
crawlinghttps://www.pomona.edu/map/?id=523#!m/54476
crawlinghttps://www.pomona.edu/directory/people/corey-leblanc
crawlinghttps://www.pomona.edu/academics/majors/computer-science
crawlinghttps://www.pomona.edu/
crawlinghttps://www.pomona.edu/admissions-aid
crawlinghttps://www.pomona.edu/academics
crawlinghttps://www.pomona.edu/life-at-pomona
crawlinghttps://www.pomona.edu/news-events
crawlinghttps://www.pomona.edu/about
crawlinghttps://www.pomona.edu/alumni-families
crawlinghttps://www.pomona.edu/directory/all
crawlinghttps://www.pomona.edu/academic-calendar
crawlinghttps://www.pomona.edu/map
crawlinghttp://catalog.pomona.edu/
crawlinghttps://www.pomona.edu/give
crawlinghttps://www.pomona.edu/new-students
crawlinghttps://www.pomona.edu/students
crawlinghttps://www.pomona.edu/faculty
crawlinghttps://www.pomona.edu/staff
crawlinghttp://social.pomona.edu/
crawlinghttps://www.pomona.edu/contact
crawlinghttps://www.pomona.edu/map/
crawlinghttps://www.pomona.edu/arts
crawlinghttps://www.pomona.edu/emergency
crawlinghttps://www.pomona.edu/employment
crawlinghttps://www.pomona.edu/support-pomona
crawlinghttps://www.pomona.edu/privacy
crawlinghttps://www.pomona.edu/website-feedback
crawlinghttp://www.pomona.edu/directory/offices-departments
crawlinghttps://www.pomona.edu/node/3014
crawlinghttps://www.pomona.edu/map/?id=523#!m/54500
crawlinghttps://www.pomona.edu/node/1447
crawlinghttp://www.cs.pomona.edu/~ebirrell/
crawlinghttps://www.pomona.edu/node/1918
crawlinghttp://www.cs.pomona.edu/~tzuyi
crawlinghttps://www.pomona.edu/node/1250
crawlinghttps://cs.pomona.edu/~ajc/
crawlinghttps://cs.pomona.edu/~ajc/arcslab/
crawlinghttps://www.pomona.edu/node/1437
crawlinghttps://research.pomona.edu/jcosborn
crawlinghttps://research.pomona.edu/faim/
crawlinghttps://www.pomona.edu/node/1517
crawlinghttp://www.cs.pomona.edu/~apapoutsaki
crawlinghttps://www.pomona.edu/node/1917
crawlinghttp://www.cs.pomona.edu/~mwu
crawlinghttps://www.pomona.edu/node/1361
crawlinghttp://pages.pomona.edu/~zyaa2019/
ignoring: http://pages.pomona.edu/~zyaa2019/
crawlinghttps://www.pomona.edu/node/5625
crawlinghttps://www.pomona.edu/node/1922
crawlinghttp://www.cs.pomona.edu/~kim/
crawlinghttps://www.pomona.edu/node/1920
crawlinghttps://www.pomona.edu/node/1912
crawlinghttps://www.pomona.edu/node/765
crawlinghttps://www.pomona.edu/academics/departments/computer-science
crawlinghttps://www.pomona.edu/academics/departments/computer-science/courses-requirements
crawlinghttps://www.pomona.edu/academics/departments/computer-science/research
crawlinghttps://www.pomona.edu/academics/departments/computer-science/colloquium
crawlinghttps://www.pomona.edu/academics/departments/computer-science/why-i-majored
crawlinghttps://www.pomona.edu/node/6270
crawlinghttps://admissions.pomona.edu/register/information
crawlinghttps://www.pomona.edu/node/6271
crawlinghttps://www.pomona.edu/academics/departments
crawlinghttps://www.pomona.edu/academics/majors/africana-studies
crawlinghttps://www.pomona.edu/academics/majors/american-studies
crawlinghttps://www.pomona.edu/academics/majors/anthropology
crawlinghttps://www.pomona.edu/academics/majors/art
crawlinghttps://www.pomona.edu/academics/majors/art-history
crawlinghttps://www.pomona.edu/academics/majors/asian-american-studies
crawlinghttps://www.pomona.edu/academics/majors/asian-studies
crawlinghttps://www.pomona.edu/academics/majors/astronomy
crawlinghttps://www.pomona.edu/academics/majors/biology
crawlinghttps://www.pomona.edu/academics/majors/chemistry
crawlinghttps://www.pomona.edu/academics/majors/chicano-latino-studies
crawlinghttps://www.pomona.edu/academics/majors/chinese
crawlinghttps://www.pomona.edu/academics/majors/classics
crawlinghttps://www.pomona.edu/academics/majors/cognitive-science
crawlinghttps://www.pomona.edu/academics/majors/dance
crawlinghttps://www.pomona.edu/academics/majors/economics
crawlinghttps://www.pomona.edu/academics/majors/english
crawlinghttps://www.pomona.edu/academics/majors/environmental-analysis
crawlinghttps://www.pomona.edu/academics/majors/french
crawlinghttps://www.pomona.edu/academics/majors/gender-womens-studies
crawlinghttps://www.pomona.edu/academics/majors/geology
crawlinghttps://www.pomona.edu/academics/majors/german-studies




In this case, BFS produced shorter links which are more reachable. Only a few of them could not be reached.Even so,
the ones that could not be totally reached were indicated by the error exception file imported, for example
ignoring: http://pages.pomona.edu/~zyaa2019/ - this link was indicated to be ignored. Generally
For DFS, it started fast then gradually slows down, and generally takes a longer time. it also gives less comprehensive
links compared to BFS which can be read clearly. For 100 URLS, BFS would be the preferred search method.
"""