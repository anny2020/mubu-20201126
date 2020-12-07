from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCaseMubuLogin(HttpRunner):

    config = Config("testcase description")\
            .variables(
            **{
               "host":"mubu.com",
               "phone":"18537810265",
               "password":"123456"}) \
            .base_url("https://$host") \
            .export("data_unique_id","JwtToken")\
            .verify(False)

    teststeps = [
        Step(
            RunRequest("/login")
            .get("/login")
            .with_headers(
                **{
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-user": "?1",
                    "sec-fetch-dest": "document",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_cookies(
                **{
                    "use-redesign": "1",
                    "language": "en-US",
                    "country": "US",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "SLARDAR_WEB_ID": "193d8f1a-e4c1-4659-917d-5404676852d4",
                }
            )
            .extract()
            .with_jmespath("cookie.data_unique_id","data_unique_id")
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/login/password")
            .get("/login/password")
            .with_headers(
                **{
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-user": "?1",
                    "sec-fetch-dest": "document",
                    "referer": "https://$host/login",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_cookies(
                **{
                    "data_unique_id": "${data_unique_id}",
                    "use-redesign": "1",
                    "_gat": "1",
                    "language": "en-US",
                    "country": "US",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "SLARDAR_WEB_ID": "0db37db8-afd6-48bb-a4c9-e112ea7daaf1",
                    "reg_prepareId": "1760871f582-1760871f556-462e-95bb-d4669dec0924",
                    "reg_focusId": "dd2da93a-2ad1-462e-95bb-1760871f969",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/api/login/submit")
                .with_variables(**{
                    "remember": True,
                    "timestamp": "${get_timestamp()}"
            })
            .post("/api/login/submit")
            .with_headers(
                **{
                    "content-length": "47",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "x-requested-with": "XMLHttpRequest",
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/login/password",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_cookies(
                **{
                    "data_unique_id": "${data_unique_id}",
                    "use-redesign": "1",
                    "language": "en-US",
                    "country": "US",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "reg_prepareId": "1760871f582-1760871f556-462e-95bb-d4669dec0924",
                    "reg_focusId": "dd2da93a-2ad1-462e-95bb-1760871f969",
                    "SLARDAR_WEB_ID": "d5dddcdf-2c48-4be6-86b3-c2cca06d8ae2",
                }
            )
            .with_data(
                {
                    "phone": "$phone",
                    "password": "$password",
                    "remember": "${remember}",
                    "token": "${get_token($phone,$password,$timestamp)"
                }
            )
            .teardown_hook("${sleep(2)}")
            .extract()
            .with_jmespath('cookies."Jwt-Token"',"JwtToken")
            .with_jmespath('cookies."user_persistence"',"user_persistance")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
            .assert_equal("body.msg", None)
            .assert_equal("body.data.next","/app")
        ),
        Step(
            RunRequest("/app")
            .get("/app")
            .with_headers(
                **{
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-user": "?1",
                    "sec-fetch-dest": "document",
                    "referer": "https://$host/login/password",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_cookies(
                **{
                    "data_unique_id": "${data_unique_id}",
                    "use-redesign": "1",
                    "reg_entrance": "https%3A%2F%2F$host%2Flist",
                    "language": "en-US",
                    "country": "US",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "reg_prepareId": "1760871f582-1760871f556-462e-95bb-d4669dec0924",
                    "reg_focusId": "dd2da93a-2ad1-462e-95bb-1760871f969",
                    "SLARDAR_WEB_ID": "d5dddcdf-2c48-4be6-86b3-c2cca06d8ae2",
                    "Jwt-Token": "${JwtToken}",
                    "user_persistence": "${user_persistance}",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/v3/")
            .get("https://api2.$host/v3/")
            .with_headers(
                **{
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "no-cors",
                    "sec-fetch-dest": "image",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_cookies(
                **{
                    "use-redesign": "1",
                    "SLARDAR_WEB_ID": "d5dddcdf-2c48-4be6-86b3-c2cca06d8ae2",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 17)
            .assert_equal("body.msg", "illegal request")
        ),
        Step(
            RunRequest("/v3/api/list/get_all_documents_page")
            .options("https://api2.$host/v3/api/list/get_all_documents_page")
            .with_headers(
                **{
                    "accept": "*/*",
                    "access-control-request-method": "POST",
                    "access-control-request-headers": "content-type,data-unique-id,jwt-token,version,x-request-id",
                    "origin": "https://$host",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            # .assert_length_greater_than("body.data.folders", 1)
        ),
        Step(
            RunRequest("/v3/api/message/get_message_unread")
            .options("https://api2.$host/v3/api/message/get_message_unread")
            .with_headers(
                **{
                    "accept": "*/*",
                    "access-control-request-method": "POST",
                    "access-control-request-headers": "content-type,data-unique-id,jwt-token,version,x-request-id",
                    "origin": "https://$host",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/v3/api/user/profile")
            .options("https://api2.$host/v3/api/user/profile")
            .with_headers(
                **{
                    "accept": "*/*",
                    "access-control-request-method": "POST",
                    "access-control-request-headers": "data-unique-id,jwt-token,version,x-request-id",
                    "origin": "https://$host",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/v3/api/list/get_all_documents_page")
            .post("https://api2.$host/v3/api/list/get_all_documents_page")
            .with_headers(
                **{
                    "content-length": "12",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "content-type": "application/json;charset=UTF-8",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "8048a241-99fc-4de0-94d8-9a07603f375e",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json({"start": ""})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
        Step(
            RunRequest("/v3/api/message/get_message_unread")
            .post("https://api2.$host/v3/api/message/get_message_unread")
            .with_headers(
                **{
                    "content-length": "10",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "content-type": "application/json;charset=UTF-8",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "aca01d57-8c17-47e2-97cf-5516c7c5fb60",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json({"page": 1})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
        Step(
            RunRequest("/v3/api/user/profile")
            .post("https://api2.$host/v3/api/user/profile")
            .with_headers(
                **{
                    "content-length": "0",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "68ef1621-8f99-4367-ae90-8a5013cd5b79",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_data("")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
        Step(
            RunRequest("/v3/api/list/item_count")
            .options("https://api2.$host/v3/api/list/item_count")
            .with_headers(
                **{
                    "accept": "*/*",
                    "access-control-request-method": "POST",
                    "access-control-request-headers": "content-type,data-unique-id,jwt-token,version,x-request-id",
                    "origin": "https://$host",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/v3/api/list/star_relation/get")
            .options("https://api2.$host/v3/api/list/star_relation/get")
            .with_headers(
                **{
                    "accept": "*/*",
                    "access-control-request-method": "GET",
                    "access-control-request-headers": "data-unique-id,jwt-token,version,x-request-id",
                    "origin": "https://$host",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/v3/api/list/item_count")
            .post("https://api2.$host/v3/api/list/item_count")
            .with_headers(
                **{
                    "content-length": "30",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "content-type": "application/json;charset=UTF-8",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "2cb822fb-9470-4b58-8988-680c3f525bef",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json({"folderId": 0, "source": "home"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
        Step(
            RunRequest("/v3/api/list/star_relation/get")
            .get("https://api2.$host/v3/api/list/star_relation/get")
            .with_headers(
                **{
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "799ae76c-57ff-4d27-9a20-9f83e75ca06d",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
        Step(
            RunRequest("/v3/api/user/get_user_params")
            .options("https://api2.$host/v3/api/user/get_user_params")
            .with_headers(
                **{
                    "accept": "*/*",
                    "access-control-request-method": "POST",
                    "access-control-request-headers": "data-unique-id,jwt-token,version,x-request-id",
                    "origin": "https://$host",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
        ),
        Step(
            RunRequest("/v3/api/user/get_user_params")
            .post("https://api2.$host/v3/api/user/get_user_params")
            .with_headers(
                **{
                    "content-length": "0",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "944be5d2-6115-4864-9a2b-af3e30c3a2d6",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_data("")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
        Step(
            RunRequest("/v3/api/list/item_count")
            .post("https://api2.$host/v3/api/list/item_count")
            .with_headers(
                **{
                    "content-length": "30",
                    "sec-ch-ua": '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
                    "data-unique-id": "f308e850-307b-11eb-9ba2-e11c5edd828e",
                    "content-type": "application/json;charset=UTF-8",
                    "accept": "application/json, text/plain, */*",
                    "jwt-token": "${JwtToken}",
                    "x-request-id": "2cb822fb-9470-4b58-8988-680c3f525bef",
                    "version": "3.0.0",
                    "origin": "https://$host",
                    "sec-fetch-site": "same-site",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://$host/",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json({"folderId": 0, "source": "home"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
    ]


if __name__ == "__main__":
    TestCaseMubuLogin().test_start()
