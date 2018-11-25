#!/usr/bin/env python

from bs4 import BeautifulSoup
from wordfish.utils import ( get_attribute, save_pretty_json )
from wikipedia import WikipediaPage
import pickle
import json
import re
import os

# Now let's derive equations from core mathematics ideas (not statistics articles)
# Organized by (AbstractTopic, PageTopic)

results = dict()

pages = [
 ( "Algrebra", "Linear algebra"),
 ( "Algrebra", "Multilinear_algebra"),
 ( "Algrebra", "Abstract algebra"),
 ( "Algrebra", "Elementary_algebra"),
 ( "Arithmetic", "Number theory"),
 ( "Calculus", "Mathematical analysis"),
 ( "Calculus", "Differential equations"),
 ( "Calculus", "Dynamical systems theory"),
 ( "Calculus", "Numerical analysis"),
 ( "Calculus", "Mathematical optimization"),
 ( "Calculus", "Functional analysis"),
 ( "Geometry", "Discrete geometry"),
 ( "Geometry", "Algebraic geometry"),
 ( "Geometry", "Analytic geometry"),
 ( "Geometry", "Differential geometry"),
 ( "Geometry", "Finite geometry"),
 ( "Geometry", "Topology"), 
 ( "Geometry", "Trigonometry"),
 ( "Foundations of Mathematics", "Philosophy of mathematics"), 
 ( "Foundations of Mathematics", "Mathematical logic"),
 ( "Foundations of Mathematics", "Set theory"),
 ( "Foundations of Mathematics", "Category theory"),
 ( "Applied Mathematics", "Mathematical physics"),
 ( "Applied Mathematics", "Probability theory"),
 ( "Applied Mathematics", "Mathematical statistics"), 
 ( "Applied Mathematics", "Statistics"),
 ( "Applied Mathematics", "Game theory"),
 ( "Applied Mathematics", "Information theory"), 
 ( "Applied Mathematics", "Computer science"),
 ( "Applied Mathematics", "Theory of computation"),
 ( "Applied Mathematics", "Control theory"),
 ( "Others", "Order theory"),
 ( "Others", "Graph theory")]


# Step 1. Get pages (and raw equations) from wikipedia

for pair in pages:
    domain = pair[0]
    method = pair[1]
    if method not in results:

        result = WikipediaPage(method)

        # Show a visual check!
        print("Matching %s to %s" %(method,result.title))
        entry = { 'categories': result.categories,
                  'title': result.title,
                  'method': method,
                  'url': result.url,
                  'summary': result.summary,
                  'images': result.images }

        # We can use links to calculate relatedness
        entry['links'] = get_attribute(result, 'links')
        entry['references'] = get_attribute(result, 'references')

        results[method] = entry


save_pretty_json(results, "wikipedia_math_articles.json")

## STEP 2: EQUATIONS ###########################################################

equations = dict()

for pair in pages:
    domain = pair[0]
    method = pair[1]
    if method not in equations:
        print("Extracting equations from %s" %(method))
        result = WikipediaPage(method)
        html = result.html()
        soup = BeautifulSoup(html, 'lxml')

        equation_list = []

        # Equations are represented as images, they map to annotations
        images = soup.findAll('img')
        for image in images:
            image_class = image.get("class")
            if image_class != None:
                if any(re.search("tex|math",x) for x in image_class):
                    png = image.get("src")
                    tex = image.get("alt")
                    entry = {"png":png,
                             "tex":tex,
                             "domain": domain,  # inefficient to store many times,
                             "topic": method}   # but more conservative
                    equation_list.append(entry)

        if len(equation_list) > 0:
            equations[method] = equation_list

# The next step is to load these equations, and map them to the space
# of characters generated from the statistics model. See the "analysis"
# subfolder for these next steps.
