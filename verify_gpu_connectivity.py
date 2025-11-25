#!/usr/bin/env python3
"""
Verify GPU Server Connectivity from CPU Server
Tests all model server endpoints and end-to-end flow
"""
import sys
import requests
import json
from typing import Dict, Any

GPU_SERVER = "192.168.51.22"
TESTS_PASSED = 0
TESTS_FAILED = 0


def print_header(title: str):
    """Print formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def test_endpoint(name: str, url: str, method: str = "GET", data: Dict[Any, Any] = None) -> bool:
    """Test an endpoint and report results"""
    global TESTS_PASSED, TESTS_FAILED

    print(f"\n[TEST] {name}")
    print(f"  URL: {url}")

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"}, timeout=30)

        if response.status_code == 200:
            print(f"  ✅ Status: {response.status_code}")
            try:
                result = response.json()
                print(f"  Response: {json.dumps(result, indent=2)[:200]}...")
            except:
                print(f"  Response: {response.text[:100]}")
            TESTS_PASSED += 1
            return True
        else:
            print(f"  ❌ Status: {response.status_code}")
            print(f"  Error: {response.text[:200]}")
            TESTS_FAILED += 1
            return False

    except requests.exceptions.Timeout:
        print(f"  ❌ Timeout after 10s")
        TESTS_FAILED += 1
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ Connection Error: {str(e)[:100]}")
        TESTS_FAILED += 1
        return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
        TESTS_FAILED += 1
        return False


def main():
    """Run all connectivity tests"""
    print_header("GPU Server Connectivity Tests")
    print(f"GPU Server: {GPU_SERVER}")
    print(f"Testing from: {requests.get('http://ifconfig.me', timeout=5).text if True else 'localhost'}")

    # Test 1: BGE-M3 Embedding Server
    print_header("Test 1: BGE-M3 Embedding Server")
    test_endpoint(
        "BGE-M3 Health Check",
        f"http://{GPU_SERVER}:8001/health"
    )

    test_endpoint(
        "BGE-M3 Embeddings",
        f"http://{GPU_SERVER}:8001/v1/embeddings",
        method="POST",
        data={"input": "test connectivity", "model": "BAAI/bge-m3"}
    )

    # Test 2: Qwen Router
    print_header("Test 2: Qwen Router Server")
    test_endpoint(
        "Qwen Health Check",
        f"http://{GPU_SERVER}:8002/health"
    )

    test_endpoint(
        "Qwen Chat Completion",
        f"http://{GPU_SERVER}:8002/v1/chat/completions",
        method="POST",
        data={
            "messages": [{"role": "user", "content": "Say 'connectivity test successful'"}],
            "max_tokens": 20,
            "temperature": 0.0
        }
    )

    # Test 3: GPT-OSS/tgw-webui
    print_header("Test 3: GPT-OSS Server")
    test_endpoint(
        "GPT-OSS Models List",
        f"http://{GPU_SERVER}:5000/v1/models"
    )

    # Test 4: Orchestrator (if running)
    print_header("Test 4: Local Orchestrator")
    test_endpoint(
        "Orchestrator Health Check",
        "http://localhost:8080/health"
    )

    test_endpoint(
        "Orchestrator End-to-End Query",
        "http://localhost:8080/query",
        method="POST",
        data={
            "query": "Test query from CPU server",
            "max_tokens": 30
        }
    )

    # Summary
    print_header("Test Summary")
    total = TESTS_PASSED + TESTS_FAILED
    print(f"\n  Total Tests: {total}")
    print(f"  ✅ Passed: {TESTS_PASSED}")
    print(f"  ❌ Failed: {TESTS_FAILED}")
    print(f"  Success Rate: {(TESTS_PASSED/total*100) if total > 0 else 0:.1f}%")

    if TESTS_FAILED == 0:
        print("\n🎉 All tests passed! GPU-CPU connectivity is working perfectly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check network configuration and firewall rules.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
