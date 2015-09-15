# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

import re

from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from flasktaggingtest.utils import flash_errors
from flasktaggingtest.public.forms import TaggingForm

blueprint = Blueprint('public', __name__, static_folder="../static")


def get_tags_choices():
    """
    Loads all saved tags, and all tags currently mapped,
    from session store.
    """

    tags_choices_all = [(str(id), title) for id, title in enumerate(session.get('tags', [])) if id]
    tags_choices = [(id, title) for id, title in tags_choices_all
            if int(id) in session.get('tag_map', [])]

    return (tags_choices_all, tags_choices)


@blueprint.route("/")
def home():
    form = TaggingForm(request.form)

    tags_choices_all, tags_choices = get_tags_choices()

    form.tags_field.choices = tags_choices_all

    form.tags_field.default = [id for id, title in tags_choices]

    # Make the new default values take effect - see:
    # http://stackoverflow.com/a/5519971/2066849
    form.tags_field.process(request.form)

    return render_template("public/home.html", form=form)


@blueprint.route("/save-tags/", methods=["POST"])
def save_tags():
    form = TaggingForm(request.form)

    tags_choices_all, tags_choices = get_tags_choices()
    tags_choices_dict = dict(tags_choices)
    tags_choices_new = []

    # Dynamically add non-recognized choices (with ID and title
    # set to the title), for select choice validation purposes.
    for v in request.form.getlist('tags_field'):
        if (
                v and
                re.match(r'^[A-Za-z0-9_\- ]+$', v) and
                not(v in tags_choices_dict)):
            tags_choices_new.append((v, v))

    form.tags_field.choices = tags_choices_all + tags_choices_new

    form.tags_field.default = [id for id, title in tags_choices]

    # Make the new default values take effect - see:
    # http://stackoverflow.com/a/5519971/2066849
    form.tags_field.process(request.form)

    if form.validate_on_submit():
        if form.tags_field.data:
            tags_ids = []

            # Find all integer IDs of submitted tags.
            for v in form.tags_field.data:
                try:
                    tag_id = int(v)
                    tags_ids.append(v)
                except ValueError:
                    pass

            # Save all tag mappings for recognized integer IDs now.
            session['tag_map'] = [int(id) for id, title in tags_choices_all if (id in tags_ids)]
            ids_found = [str(id) for id in session['tag_map']]

            for v in form.tags_field.data:
                # Cases where a submitted tag ID is either
                # a non-integer, or where tag lookup by ID failed.
                if not (v in ids_found):
                    # Try and do tag lookup by title.
                    try:
                        existing_tag = [int(id) for id, title in tags_choices_all if (title == v)][0]
                    except IndexError:
                        existing_tag = None

                    if existing_tag:
                        # If tag lookup by title succeeded, then
                        # add the tag ID to the mapping.
                        session['tag_map'].append(existing_tag)
                    elif re.match(r'^[A-Za-z0-9_\- ]+$', v):
                        if not session.get('tags'):
                            session['tags'] = ['']

                        # Otherwise, create a new tag, and map it.
                        session['tags'].append(v)
                        new_tag = len(session['tags'])-1

                        session['tag_map'].append(new_tag)
        else:
            session['tag_map'] = []

        flash("Tags saved.", 'success')
    else:
        flash_errors(form)

    return redirect(url_for("public.home"))
