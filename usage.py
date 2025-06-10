TURNSTILE_URL = "http://turn.prayogatri.my.id"
API_KEY = "<APIKEY>"

def solve_turnstile():
    try:
        # Step 1: Submit task
        response = requests.get(f"{TURNSTILE_URL}/turnstile", params={
            "url": "https://klokapp.ai",
            "sitekey": "0x4AAAAAABdQypM3HkDQTuaO",
            "key": API_KEY
        })
        response.raise_for_status()
        task_id = response.json()["task_id"]
    except requests.RequestException as e:
        print(f"Error submitting task: {e}")
        return

    # Step 2: Poll for result
    timeout = time.time() + 60
    while True:
        try:
            response = requests.get(f"{TURNSTILE_URL}/result", params={
                "id": task_id,
                "key": API_KEY
            })
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as e:
            print(f"Error fetching result: {e}")
            break

        if result["status"] == "success":
            print(f"Turnstile Token: {result['value']}")
            break
        elif result["status"] == "fail":
            print("Turnstile solving failed")
            break
        else:
            print("Waiting for solution...")
            if time.time() > timeout:
                print("Timeout while waiting for solution.")
                break
            time.sleep(2)

def usage_recaptcha():
    RECAPTCHA_URL = "https://rev2.prayogatri.my.id"
    API_KEY = "<APIKEY>"
    try:
        response = requests.post(
            f"{RECAPTCHA_URL}/solve",
            params={"key": API_KEY},
            json={
                "url": "https://faucet.gokite.ai/api/sendToken",
                "site_key": "6LeNaK8qAAAAAHLuyTlCrZD_U1UoFLcCTLoa_69T",
                "headless": True
            }
        )
        response.raise_for_status()
        result = response.json()
        print("/solve result:")
        print(result)
    except requests.RequestException as e:
        print(f"Error calling /solve: {e}")

solve_turnstile()
usage_recaptcha()
