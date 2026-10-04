from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Controlled Defective Target Web Application")

# HTML Templates
LANDING_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Defective Target Store - Benchmark Application</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
        .card { background: #1e293b; padding: 24px; border-radius: 12px; max-width: 600px; margin: 0 auto 20px; border: 1px solid #334155; }
        a, button { color: #38bdf8; text-decoration: none; display: inline-block; margin-top: 10px; cursor: pointer; }
        button { background: #38bdf8; color: #000; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; }
        input { padding: 8px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; width: 100%; box-sizing: border-box; margin-bottom: 12px; }
        .danger-btn { background: #f43f5e; color: #fff; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Autonomous QA Target Sandbox</h1>
        <p>This benchmark application contains interactive flows and intentional functional defects for testing the Autonomous QA Agent.</p>
        <div style="display: flex; gap: 10px; margin-top: 20px;">
            <a href="/login"><button>Go to Login Portal</button></a>
            <a href="/checkout"><button>Go to Checkout Form</button></a>
            <a href="/modal"><button>Go to Modal Sandbox</button></a>
            <a href="/crash"><button class="danger-btn">Go to Crash Trigger</button></a>
        </div>
    </div>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>User Login Portal</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
        .card { background: #1e293b; padding: 24px; border-radius: 12px; max-width: 400px; margin: 0 auto; border: 1px solid #334155; }
        input { padding: 10px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; width: 100%; box-sizing: border-box; margin-bottom: 12px; }
        button { background: #10b981; color: #000; border: none; padding: 10px 16px; border-radius: 6px; font-weight: bold; width: 100%; cursor: pointer; }
        .success { color: #10b981; display: none; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>User Login</h2>
        <form id="login-form" onsubmit="event.preventDefault(); document.getElementById('login-success').style.display='block';">
            <label>Username</label>
            <input type="text" id="username" name="username" placeholder="admin" required />
            <label>Password</label>
            <input type="password" id="password" name="password" placeholder="••••••••" required />
            <button type="submit" id="btn-login">Sign In</button>
        </form>
        <div id="login-success" class="success">Authentication Successful! Welcome back.</div>
        <p><a href="/" style="color: #94a3b8; font-size: 12px;">Back to Home</a></p>
    </div>
</body>
</html>
"""

CHECKOUT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Order Checkout</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
        .card { background: #1e293b; padding: 24px; border-radius: 12px; max-width: 450px; margin: 0 auto; border: 1px solid #334155; }
        input { padding: 8px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; width: 100%; box-sizing: border-box; margin-bottom: 12px; }
        button { background: #38bdf8; color: #000; border: none; padding: 10px 16px; border-radius: 6px; font-weight: bold; width: 100%; cursor: pointer; }
        .error-box { background: #f43f5e20; border: 1px solid #f43f5e; color: #f43f5e; padding: 10px; border-radius: 6px; display: none; margin-top: 10px; }
    </style>
    <script>
        async function applyCoupon() {
            const coupon = document.getElementById('coupon-code').value;
            const res = await fetch('/api/checkout/apply-coupon', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ coupon: coupon })
            });
            if (!res.ok) {
                const box = document.getElementById('error-box');
                box.style.display = 'block';
                box.innerText = 'Server Error: ' + res.status + ' during coupon verification!';
                throw new Error('HTTP ' + res.status + ' Internal Server Error');
            }
        }
    </script>
</head>
<body>
    <div class="card">
        <h2>Order Checkout ($49.00)</h2>
        <label>Coupon Code (Intentional Bug: blank or 'DISCOUNT50' throws 500)</label>
        <input type="text" id="coupon-code" name="coupon" placeholder="Leave empty or DISCOUNT50" />
        <button id="btn-apply-coupon" onclick="applyCoupon()">Apply Coupon & Place Order</button>
        <div id="error-box" class="error-box"></div>
        <p><a href="/" style="color: #94a3b8; font-size: 12px;">Back to Home</a></p>
    </div>
</body>
</html>
"""

MODAL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Modal Sandbox</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
        .card { background: #1e293b; padding: 24px; border-radius: 12px; max-width: 450px; margin: 0 auto; border: 1px solid #334155; }
        button { background: #a855f7; color: #fff; border: none; padding: 10px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        #modal-dialog { display: none; background: #334155; padding: 20px; border-radius: 8px; margin-top: 15px; border: 1px solid #64748b; }
    </style>
    <script>
        function toggleModal() {
            // Intentional bug: removes modal from DOM instead of toggling visibility
            const dialog = document.getElementById('modal-dialog');
            if (dialog) {
                dialog.style.display = 'block';
                // Trigger defect: self destruct after 50ms
                setTimeout(() => { dialog.remove(); }, 50);
            }
        }
    </script>
</head>
<body>
    <div class="card">
        <h2>Dynamic Modal Bug Test</h2>
        <p>Tests DOM persistence when triggering interactive overlays.</p>
        <button id="btn-open-modal" onclick="toggleModal()">Open Dynamic Modal</button>
        <div id="modal-dialog">
            <h3>Modal Dialog Surface</h3>
            <p>This dialogue is supposed to stay open until dismissed.</p>
        </div>
        <p><a href="/" style="color: #94a3b8; font-size: 12px;">Back to Home</a></p>
    </div>
</body>
</html>
"""

CRASH_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Client Crash Test</title>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
        .card { background: #1e293b; padding: 24px; border-radius: 12px; max-width: 450px; margin: 0 auto; border: 1px solid #334155; }
        button { background: #f43f5e; color: #fff; border: none; padding: 10px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style>
    <script>
        function triggerJsCrash() {
            // Intentional JavaScript Uncaught TypeError
            const authState = undefined;
            console.log(authState.session.token); // Will throw Uncaught TypeError
        }
    </script>
</head>
<body>
    <div class="card">
        <h2>Uncaught JavaScript Exception Test</h2>
        <p>Clicking the button below invokes an unhandled null pointer in client-side code.</p>
        <button id="btn-trigger-crash" onclick="triggerJsCrash()">Trigger Uncaught Exception</button>
        <p><a href="/" style="color: #94a3b8; font-size: 12px;">Back to Home</a></p>
    </div>
</body>
</html>
"""

# Routes
@app.get("/", response_class=HTMLResponse)
async def landing():
    return LANDING_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return LOGIN_HTML

@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page():
    return CHECKOUT_HTML

@app.get("/modal", response_class=HTMLResponse)
async def modal_page():
    return MODAL_HTML

@app.get("/crash", response_class=HTMLResponse)
async def crash_page():
    return CRASH_HTML

class CouponPayload(BaseModel):
    coupon: Optional[str] = None

@app.post("/api/checkout/apply-coupon")
async def apply_coupon(payload: CouponPayload):
    # Intentional Bug: empty string or 'DISCOUNT50' causes unhandled server 500 error
    if not payload.coupon or payload.coupon.strip() == "" or payload.coupon == "DISCOUNT50":
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: KeyError 'discount_rate' in coupon_engine.py at line 58"
        )
    return {"status": "success", "discount": 10.0}

@app.get("/api/buggy-data")
async def buggy_data():
    # Intentional 500 endpoint
    raise HTTPException(status_code=500, detail="Database connection pool exhausted")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8088, reload=False)
