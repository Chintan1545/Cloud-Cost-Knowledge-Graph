CREATE CONSTRAINT unique_resource IF NOT EXISTS
FOR (r:Resource)
REQUIRE r.id IS UNIQUE;

CREATE INDEX service_name_index IF NOT EXISTS
FOR (s:Service)
ON (s.name);

CREATE INDEX cost_env_index IF NOT EXISTS
FOR (c:CostRecord)
ON (c.environment);