# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import absolute_import

from pex.compatibility import Iterable
from pex.compatibility import string as compatibility_string
from pex.third_party.pkg_resources import Requirement

REQUIRED_ATTRIBUTES = (
    'extras',
    'key',
    'project_name',
    'specs',
)


def quacks_like_req(req):
  return all(hasattr(req, attr) for attr in REQUIRED_ATTRIBUTES)


def maybe_requirement(req):
  if isinstance(req, Requirement) or quacks_like_req(req):
    return req
  elif isinstance(req, compatibility_string):
    return Requirement.parse(req)
  raise ValueError('Unknown requirement %r' % (req,))


def maybe_requirement_list(reqs):
  if isinstance(reqs, (compatibility_string, Requirement)) or quacks_like_req(reqs):
    return [maybe_requirement(reqs)]
  elif isinstance(reqs, Iterable):
    return [maybe_requirement(req) for req in reqs]
  raise ValueError('Unknown requirement list %r' % (reqs,))


def requirement_is_exact(req):
  return bool(req.specs and len(req.specs) == 1 and req.specs[0][0] == '==')
