import unittest
from unittest.mock import patch
from resolve_source import resolve


class ResolveTest(unittest.TestCase):
    def test_acceptance_uses_requested_commit(self):
        with patch('resolve_source.git', return_value='a'*40):
            self.assertEqual(resolve('workflow_dispatch', 'feature', 'acceptance-check', ''), ('a'*40,'acceptance-check',False))
    def test_release_peels_tag_when_ref_omitted(self):
        with patch('resolve_source.git', return_value='b'*40) as git:
            self.assertEqual(resolve('workflow_dispatch', '', 'v1.2.3', '')[2],True)
            self.assertIn('refs/tags/v1.2.3^{commit}',git.call_args.args)
    def test_mismatched_release_fails(self):
        with patch('resolve_source.git', side_effect=['a'*40,'','b'*40]):
            with self.assertRaisesRegex(ValueError,'exact release tag'):resolve('workflow_dispatch','main','v1.2.3','')
    def test_matching_release_succeeds(self):
        with patch('resolve_source.git', return_value='a'*40):
            self.assertTrue(resolve('workflow_dispatch','main','v1.2.3','')[2])
    def test_invalid_tag_fails(self):
        with patch('resolve_source.git', return_value='a'*40):
            with self.assertRaises(ValueError):resolve('workflow_dispatch','branch','acceptance-x\nlatest','')
    def test_acceptance_requires_ref(self):
        with self.assertRaises(ValueError):resolve('workflow_dispatch','','','')
    def test_acceptance_fetches_non_default_branch(self):
        with patch('resolve_source.git', return_value='a'*40) as git:
            resolve('workflow_dispatch','feature/sandbox','acceptance-branch','')
            git.assert_any_call('fetch','--no-tags','origin','feature/sandbox')
    def test_option_like_ref_is_rejected(self):
        with self.assertRaises(ValueError):resolve('workflow_dispatch','--upload-pack=bad','acceptance-x','')


if __name__=='__main__':unittest.main()
