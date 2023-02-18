import pytest
from dbt.tests.util import run_dbt

models_file_model_sql = """
{{ config(materialized='table') }}
select *
from read_csv_auto('github://data/team_ratings.csv')
WHERE conf = 'West'
"""


class TestFilesystems:
    @pytest.fixture(scope="class")
    def dbt_profile_target(self):
        return {
            "type": "duckdb",
            "path": ":memory:",
            "filesystems": [{"fs": "github", "org": "jwills", "repo": "nba_monte_carlo"}],
        }

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "file_model.sql": models_file_model_sql,
        }

    def test_filesystems(self, project):
        results = run_dbt()
        assert len(results) == 1
