import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from storage import Store
from records import Records
from sample_data import seed
from analysis import dataset,summary,group_summary,subset,patterns
from charts import category_chart,player_chart

class ProjectTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.r=Records(Store(self.tmp.name))
 def tearDown(self):self.tmp.cleanup()
 def test_empty(self):self.assertEqual(summary(dataset(self.r))['attempts'],0)
 def test_seed(self):
  self.assertTrue(seed(self.r));self.assertFalse(seed(self.r));self.assertEqual(len(self.r.all('results')),16)
 def test_crud(self):
  pid=self.r.put('players',{'name':'Test','age':'25'});self.r.put('players',{'name':'New','age':'25'},pid);self.assertEqual(self.r.all('players')[0]['name'],'New');self.r.delete('players',pid);self.assertFalse(self.r.all('players'))
 def test_validation(self):
  with self.assertRaises(ValueError):self.r.put('players',{'name':'','age':'20'})
  with self.assertRaises(ValueError):self.r.put('players',{'name':'OK','age':'abc'})
  with self.assertRaises(ValueError):self.r.put('puzzles',{'title':'X','category':'Invalid','difficulty':'Easy'})
 def test_references_and_delete(self):
  seed(self.r);pid=self.r.all('players')[0]['player_id']
  with self.assertRaises(ValueError):self.r.delete('players',pid)
 def test_aggregates(self):
  seed(self.r);d=dataset(self.r);self.assertEqual(summary(d)['attempts'],16);self.assertEqual(len(group_summary(d,'category')),4)
 def test_filters(self):
  seed(self.r);d=dataset(self.r);self.assertEqual(len(subset(d,category='Crossword')),4);self.assertEqual(len(subset(d,query='Daily Grid')),4)
 def test_charts(self):
  seed(self.r);d=dataset(self.r);self.assertTrue(category_chart(d));self.assertTrue(player_chart(d))
 def test_bad_result(self):
  seed(self.r);record=self.r.all('results')[0];record['score']='nan';rows=self.r.all('results');rows[0]=record;self.r.store.save('results',rows)
  with self.assertRaises(ValueError):dataset(self.r)
 def test_patterns(self):seed(self.r);self.assertIn('Longest average',patterns(dataset(self.r)))

if __name__=='__main__':unittest.main()
