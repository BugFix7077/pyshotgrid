import datetime
import os

import pytest
from shotgun_api3.lib import mockgun


@pytest.fixture(scope="module")
def sg():
    resources_dir = os.path.join(os.path.dirname(__file__), "resources")

    mockgun_schema_dir = os.path.join(resources_dir, "mockgun_schemas")
    mockgun.Shotgun.set_schema_paths(
        os.path.join(mockgun_schema_dir, "schema.db"),
        os.path.join(mockgun_schema_dir, "entity_schema.db"),
    )
    sg = mockgun.Shotgun(
        base_url="https://test.shotgunstudio.com",
        script_name="Unittest User",
        api_key="$ome_password",
    )

    add_default_entities(sg)

    return sg


def add_default_entities(sg):
    # HumanUsers
    person_a = sg.create(
        "HumanUser",
        {
            "firstname": "Alice",
            "lastname": "Alpha",
            "name": "Alice Alpha",
            "login": "alice.alpha",
            "email": "alice@company.com",
        },
    )
    person_b = sg.create(
        "HumanUser",
        {
            "firstname": "Bob",
            "lastname": "Beta",
            "name": "Bob Beta",
            "login": "bob.beta",
            "email": "bob@company.com",
        },
    )
    person_c = sg.create(
        "HumanUser",
        {
            "firstname": "Carol",
            "lastname": "Clown",
            "name": "Carol Clown",
            "login": "carol.clown",
            "email": "carol@company.com",
        },
    )
    sg.create(
        "HumanUser",
        {
            "firstname": "Dan",
            "lastname": "Deactivated",
            "name": "Dan Deactivated",
            "login": "dan.deactivated",
            "email": "dan@company.com",
            "sg_status_list": "dis",
        },
    )

    # LocalStorages
    local_storage = sg.create(
        "LocalStorage",
        {
            "code": "primary",
            "mac_path": "/Volumes/projects",
            "windows_path": "P:\\",
            "linux_path": "/mnt/projects",
        },
    )

    # Pipeline Steps
    pipeline_step_cmp = sg.create("Step", {"code": "Compositing", "short_name": "CMP"})
    pipeline_step_lgt = sg.create("Step", {"code": "Lighting", "short_name": "LGT"})
    pipeline_step_mdl = sg.create("Step", {"code": "Modeling", "short_name": "MDL"})

    # Projects
    project_a = sg.create(
        "Project",
        {
            "name": "Test Project A",
            "tank_name": "tpa",
            "users": [person_a, person_b, person_c],
        },
    )
    project_b = sg.create(
        "Project",
        {
            "name": "Test Project B",
            "tank_name": "tpb",
            "users": [person_a, person_b, person_c],
        },
    )

    sg.update("HumanUser", 1, {"projects": [project_a, project_b]})
    sg.update("HumanUser", 2, {"projects": [project_a, project_b]})
    sg.update("HumanUser", 3, {"projects": [project_a, project_b]})
    sg.update("HumanUser", 4, {"projects": [project_a, project_b]})

    # Assets
    asset_tree_a = sg.create("Asset", {"code": "Tree", "project": project_a})
    sg.create("Asset", {"code": "CarA", "project": project_a})
    sg.create("Asset", {"code": "CarB", "project": project_a})

    # Sequences
    sq111 = sg.create("Sequence", {"code": "sq111", "project": project_a})
    sq222 = sg.create("Sequence", {"code": "sq222", "project": project_a})

    # Shots
    shot_a = sg.create("Shot", {"code": "sq111_sh1111", "project": project_a, "sg_sequence": sq111})
    shot_b = sg.create("Shot", {"code": "sq111_sh2222", "project": project_a, "sg_sequence": sq111})
    sg.create("Shot", {"code": "sq222_sh3333", "project": project_a, "sg_sequence": sq222})
    sg.create("Shot", {"code": "sq222_sh4444", "project": project_a, "sg_sequence": sq222})

    # Tasks
    task_cmp_a = sg.create(
        "Task",
        {
            "content": "comp",
            "project": project_a,
            "entity": shot_a,
            "step": pipeline_step_cmp,
            "task_assignees": [person_a],
        },
    )
    sg.create(
        "Task",
        {
            "content": "comp",
            "project": project_a,
            "entity": shot_b,
            "step": pipeline_step_cmp,
            "task_assignees": [person_a],
        },
    )
    task_lgt_a = sg.create(
        "Task",
        {
            "content": "lighting",
            "project": project_a,
            "entity": shot_a,
            "step": pipeline_step_lgt,
            "task_assignees": [person_a],
        },
    )
    task_mdl_a = sg.create(
        "Task",
        {
            "content": "modeling",
            "project": project_a,
            "entity": asset_tree_a,
            "step": pipeline_step_mdl,
            "task_assignees": [person_b],
        },
    )

    # PublishedFileTypes
    pub_type_alembic = sg.create("PublishedFileType", {"code": "Alembic Cache"})
    pub_type_render = sg.create("PublishedFileType", {"code": "Rendered Image"})

    # PublishedFiles
    for i in range(1, 6):
        sg.create(
            "PublishedFile",
            {
                "code": "sh1111_city_v{:03d}.%04d.exr".format(i),
                "name": "sh1111_city",
                "version_number": i,
                "published_file_type": pub_type_render,
                "project": project_a,
                "task": task_cmp_a,
                "entity": shot_a,
                "path_cache": "tp/sequences/sq111/sh1111_city_v{:03d}.%04d.exr".format(i),
                "path_cache_storage": local_storage,
                "created_by": person_a,
            },
        )
    for i in range(1, 6):
        sg.create(
            "PublishedFile",
            {
                "code": "sh1111_city_v{:03d}.abc".format(i),
                "name": "sh1111_city",
                "version_number": i,
                "published_file_type": pub_type_alembic,
                "project": project_a,
                "task": task_lgt_a,
                "entity": shot_a,
                "path_cache": "tp/sequences/sq111/sh1111_city_v{:03d}.abc".format(i),
                "path_cache_storage": local_storage,
                "created_by": person_b,
            },
        )
    for i in range(1, 6):
        sg.create(
            "PublishedFile",
            {
                "code": "Tree_mdl_v{:03d}.abc".format(i),
                "name": "Tree_mdl",
                "version_number": i,
                "published_file_type": pub_type_alembic,
                "project": project_a,
                "task": task_mdl_a,
                "entity": asset_tree_a,
                "path_cache": "tp/asset/prop/Tree_mdl_v{:03d}.abc".format(i),
                "path_cache_storage": local_storage,
                "created_by": person_b,
            },
        )

    # Playlists
    playlist_a = sg.create("Playlist", {"code": "Playlist A", "project": project_a})
    playlist_b = sg.create("Playlist", {"code": "Playlist B", "project": project_b})
    sg.create("Playlist", {"code": "Playlist C"})

    # PipelineConfigurations
    sg.create("PipelineConfiguration", {"code": "Primary"})
    sg.create("PipelineConfiguration", {"code": "Primary", "project": project_a})
    sg.create("PipelineConfiguration", {"code": "Develop", "project": project_a})

    # Notes
    sg.create("Note", {"subject": "Test note"})

    # Versions
    sg.create(
        "Version",
        {
            "code": "sh1111_city_v001",
            "user": person_a,
            "created_at": datetime.datetime(2000, 1, 1, 12, 0, 0),
            "sg_task": task_cmp_a,
            "entity": shot_a,
            "project": project_a,
            "playlists": [playlist_a],
        },
    )
    sg.create(
        "Version",
        {
            "code": "sh1111_city_v002",
            "user": person_a,
            "created_at": datetime.datetime(2000, 1, 2, 12, 0, 0),
            "sg_task": task_cmp_a,
            "entity": shot_a,
            "project": project_a,
            "playlists": [playlist_a],
        },
    )
    sg.create(
        "Version",
        {
            "code": "Tree_mdl_v001",
            "user": person_b,
            "created_at": datetime.datetime(2000, 1, 1, 12, 0, 0),
            "sg_task": task_mdl_a,
            "entity": asset_tree_a,
            "project": project_a,
            "playlists": [playlist_b],
        },
    )
