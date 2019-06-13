from treetagger import TreeTagger
from pprint import pprint

tt_pt = TreeTagger(language='portuguese2')
pprint(tt_pt.tag('Minha namorada é maravilhosa, gostosa, musa do verão!'))
