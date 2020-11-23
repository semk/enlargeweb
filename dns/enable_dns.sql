/*
 * This PostgreSQL function converts IP address packed to unsigned long
 * to ordinary dotted string, e.g. "127.0.0.1"
 */
CREATE LANGUAGE 'plpgsql'
CREATE OR REPLACE FUNCTION ulongToIpStr(ip BIGINT) RETURNS TEXT AS $$
DECLARE
	res TEXT := '';
	tmp BIGINT;
	BEGIN
		tmp := ip;
		res := (tmp & 255);
		FOR i IN 1..3 LOOP
			tmp := tmp >> 8;
			res := (tmp & 255) || '.' || res;
		END LOOP;
		RETURN res;
	END;
$$ LANGUAGE plpgsql;

/*
 * Example initial deploy zone configuration
 */
INSERT INTO dpsrv.dns_records(
	zone,
	host,
	ttl,
	type,
	data,
	resp_person,
	serial,
	refresh,
	retry,
	expire,
	minimum,
	mx_priority
) VALUES (
	'deploy',
	'@',
	1000000,
	'soa',
	'deploy',
	'nickv@parallels.com',
	2008122601,
	28800,
	14400,
	604800,
	86400,
	20
);
