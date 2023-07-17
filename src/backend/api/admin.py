# Copyright 2023 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Annotated, List

from fastapi import Depends
from fastapi.routing import APIRouter

import backend.admin_ops.types as admin_ops_types
import backend.admin_ops.users as admin_ops_users
from backend.api import S3GWClient, s3gw_client, s3gw_client_responses

router = APIRouter(prefix="/admin")

S3GWClientDep = Annotated[S3GWClient, Depends(s3gw_client)]


@router.get(
    "/userInfo",
    response_model=admin_ops_types.UserInfo,
    responses=s3gw_client_responses(),
)
async def get_user_info(
    conn: S3GWClientDep, uid: str, with_statistics: bool
) -> admin_ops_types.UserInfo:
    res = await admin_ops_users.get_user_info(
        conn.endpoint, conn.access_key, conn.secret_key, uid, with_statistics
    )
    return res


@router.put(
    "/userCreate",
    response_model=admin_ops_types.UserInfo,
    responses=s3gw_client_responses(),
)
async def create_user(
    conn: S3GWClientDep,
    uid: str,
    display_name: str,
    email: str,
    key_type: str,
    access_key: str,
    secret_key: str,
    user_caps: str,
    generate_key: bool,
    max_buckets: int,
    suspended: bool,
    tenant: str,
) -> admin_ops_types.UserInfo:
    res = await admin_ops_users.create(
        conn.endpoint,
        conn.access_key,
        conn.secret_key,
        user=admin_ops_types.UserOpParams(
            uid=uid,
            display_name=display_name,
            email=email,
            key_type=key_type,
            access_key=access_key,
            secret_key=secret_key,
            user_caps=user_caps,
            generate_key=generate_key,
            max_buckets=max_buckets,
            suspended=suspended,
            tenant=tenant,
        ),
    )
    return res


@router.delete(
    "/userDelete",
    responses=s3gw_client_responses(),
)
async def delete_user(conn: S3GWClientDep, uid: str) -> None:
    res = await admin_ops_users.delete(
        conn.endpoint, conn.access_key, conn.secret_key, uid=uid
    )
    return res


@router.get(
    "/userIsAuthAdmin",
    response_model=admin_ops_types.AuthUser,
    responses=s3gw_client_responses(),
)
async def get_auth_user(conn: S3GWClientDep) -> admin_ops_types.AuthUser:
    res = await admin_ops_users.get_auth_user(
        conn.endpoint, conn.access_key, conn.secret_key
    )
    return res


@router.get(
    "/userListUserIDs",
    response_model=List[str],
    responses=s3gw_client_responses(),
)
async def list_uids(conn: S3GWClientDep) -> List[str]:
    res = await admin_ops_users.list_uids(
        conn.endpoint, conn.access_key, conn.secret_key
    )
    return res


@router.put(
    "/userCreateKey",
    response_model=List[admin_ops_types.UserKeys],
    responses=s3gw_client_responses(),
)
async def create_key(
    conn: S3GWClientDep,
    uid: str,
    key_type: str,
    access_key: str,
    secret_key: str,
    generate_key: bool,
) -> List[admin_ops_types.UserKeys]:
    res = await admin_ops_users.create_key(
        conn.endpoint,
        conn.access_key,
        conn.secret_key,
        key_params=admin_ops_types.UserKeyOpParams(
            uid=uid,
            key_type=key_type,
            access_key=access_key,
            secret_key=secret_key,
            generate_key=generate_key,
        ),
    )
    return res


@router.get(
    "/userGetAllKeys",
    response_model=List[admin_ops_types.UserKeys],
    responses=s3gw_client_responses(),
)
async def get_keys(
    conn: S3GWClientDep, uid: str
) -> List[admin_ops_types.UserKeys]:
    res = await admin_ops_users.get_keys(
        conn.endpoint, conn.access_key, conn.secret_key, uid=uid
    )
    return res


@router.delete(
    "/userDeleteKey",
    responses=s3gw_client_responses(),
)
async def delete_key(
    conn: S3GWClientDep, uid: str, user_access_key: str
) -> None:
    await admin_ops_users.delete_key(
        conn.endpoint,
        conn.access_key,
        conn.secret_key,
        uid=uid,
        user_access_key=user_access_key,
    )


@router.put(
    "/userUpdateQuota",
    responses=s3gw_client_responses(),
)
async def quota_update(
    conn: S3GWClientDep,
    uid: str,
    max_objects: int,
    max_size: int,
    quota_type: str,
    enabled: bool,
) -> None:
    if quota_type != "user":
        return

    await admin_ops_users.quota_update(
        conn.endpoint,
        conn.access_key,
        conn.secret_key,
        uid=uid,
        quota=admin_ops_types.UserQuotaOpParams(
            max_objects=max_objects,
            max_size=max_size,
            quota_type="user",
            enabled=enabled,
        ),
    )