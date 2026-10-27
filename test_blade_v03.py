import unittest
from blade_v03 import from_tree,from_flat,render_md,validate_md
class Tests(unittest.TestCase):
 def test_tree_branch_and_lossless(self):
  tree={'current_node':'c','mapping':{'a':{'parent':None,'message':None},'b':{'parent':'a','message':{'id':'b','author':{'role':'user'},'content':{'content_type':'text','parts':['a\\n\` ~ \\\\ Ω']}}},'c':{'parent':'b','message':{'id':'c','author':{'role':'assistant'},'content':{'content_type':'text','parts':['hello',' world']}}},'d':{'parent':'b','message':{'id':'d','author':{'role':'assistant'},'content':{'parts':['OFF BRANCH']}}}}}
  rows,meta=from_tree(tree);self.assertEqual([r['id'] for r in rows],['b','c']);self.assertEqual(meta['nonactive_nodes'],1);self.assertTrue(validate_md(render_md(rows,'x'),rows))
 def test_flat_contents(self):
  rows=from_flat([{'id':'x','role':'assistant','contents':[{'type':'text','content':'hi'},{'type':'text','content':' there'}]}]);self.assertEqual(rows[0]['text'],'hi there');self.assertTrue(validate_md(render_md(rows,'y'),rows))
if __name__=='__main__':unittest.main()
