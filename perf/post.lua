-- post.lua: rotate through JSON lines from a file (bodies.jsonl)
local path = os.getenv("BODIES") or "data/generated/bodies_100.jsonl"
local file = io.open(path, "r")
if not file then
  error("Cannot open bodies file: " .. path)
end
local bodies = {}
for line in file:lines() do
  if #line > 2 then table.insert(bodies, line) end
end
file:close()

local n = 0
request = function()
  n = (n % #bodies) + 1
  wrk.method = "POST"
  wrk.headers["Content-Type"] = "application/json"
  wrk.body = bodies[n]
  return wrk.format(nil, "/predict")
end
