---
title: owasp juice shop > npm audit
categories: owasp juice shop
---
In this post, we will audit the OWASP juice shop app with npm. You should have already cloned the juice 
shop code and installed the modules with NPM. Some familiarity with jq for filtering json is assumed.

# Audit

Let's run the audit command.
```
networkandcode@ubuntu20:~/juice-shop$ npm audit
npm ERR! code EAUDITNOLOCK
npm ERR! audit Neither npm-shrinkwrap.json nor package-lock.json found: Cannot audit a project without a lockfile
npm ERR! audit Try creating one first with: npm i --package-lock-only

npm ERR! A complete log of this run can be found in:
npm ERR!     /home/networkandcode/.npm/_logs/2021-08-07T09_55_10_522Z-debug.log
```

It throws an error as there is no package.lock in the directory. We can generate it using the reference 
command given above.
```
$ npm i --package-lock-only
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@^2.1.2 (node_modules/jest-haste-map/node_modules/fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@2.3.2: wanted {"os":"darwin","arch":"any"} (current: {"os":"linux","arch":"x64"})

audited 2005 packages in 30.644s

117 packages are looking for funding
  run `npm fund` for details

found 25 vulnerabilities (3 low, 10 moderate, 9 high, 3 critical)
  run `npm audit fix` to fix them, or `npm audit` for details
```

The output above shows this app has 25 vulnerabilities, we can get more details about those using the 
npm audit command.
```
$ npm audit
---TRUNCATED--
  High            Arbitrary File Creation/Overwrite via insufficient symlink    
                  protection due to directory cache poisoning                   
                                                                                
  Package         tar                                                           
                                                                                
  Patched in      >=3.2.3 <4.0.0 || >=4.4.15  <5.0.0 || >=5.0.7 <6.0.0 ||       
                  >=6.1.2                                                       
                                                                                
  Dependency of   sqlite3                                                       
                                                                                
  Path            sqlite3 > node-gyp > tar                                      
                                                                                
  More info       https://npmjs.com/advisories/1771  
---TRUNCATED---
```

The detail of one of the vulnerabilities is shown above. The exit code of the previous command can be 
checked, it would be 1 meaning it failed, as there are vulnerabilities.
```
$ echo $?
1
```
This is useful in CI pipelines, where the npm audit stage would be failed or passed according to the 
exit code.

# JSON
Its sometimes handy to store the results in a json file that filtering easier.
```
$npm audit --json > /tmp/auditresult.json
$ echo $?
1
```

The exit code above is still 1 meaning it failed because of vulnerabilities. Let's try fitelring with 
jq.

We can traverse through the following main keys
```
$ cat /tmp/auditresult.json | jq 'keys'
[
  "actions",
  "advisories",
  "metadata",
  "muted",
  "runId"
]

```

Let's see what are the keys in advisories.
```
$ cat /tmp/auditresult.json | jq '.advisories' | jq 'keys'
[
  "1065",
  "1122",
  "135",
  "1523",
  "154",
  "1673",
  "1675",
  "1676",
  "17",
  "1769",
  "1770",
  "1771",
  "532",
  "55",
  "577",
  "658",
  "782",
  "88"
]
```

Let's pick the last one 88.
```
$ cat /tmp/auditresult.json | jq '.advisories."88"' | jq keys
[
  "access",
  "created",
  "cves",
  "cwe",
  "deleted",
  "findings",
  "found_by",
  "id",
  "metadata",
  "module_name",
  "overview",
  "patched_versions",
  "recommendation",
  "references",
  "reported_by",
  "severity",
  "title",
  "updated",
  "url",
  "vulnerable_versions"
]
```

We shall check the associated cves of this vulnerability
```
$ cat /tmp/auditresult.json | jq '.advisories."88".cves'
[
  "CVE-2016-1000223"
]
```

Or we can get it's complete details.
```
$ cat /tmp/auditresult.json | jq '.advisories."88"'
{
  "findings": [
    {
      "version": "0.2.6",
      "paths": [
        "express-jwt>jsonwebtoken>jws",
        "jsonwebtoken>jws"
      ]
    }
  ],
  "id": 88,
  "created": "2016-03-22T16:50:45.816Z",
  "updated": "2019-06-24T15:15:36.951Z",
  "deleted": null,
  "title": "Forgeable Public/Private Tokens",
  "found_by": {
    "name": "Brian Brennan and Tim McLean"
  },
  "reported_by": {
    "name": "Brian Brennan and Tim McLean"
  },
  "module_name": "jws",
  "cves": [
    "CVE-2016-1000223"
  ],
  "vulnerable_versions": "<3.0.0",
  "patched_versions": ">=3.0.0",
  "overview": "Affected versions of the `jws` package allow users to select what algorithm the server will use to verify a provided JWT. A malicious actor can use this behaviour to arbitrarily modify the contents of a JWT while still passing verification. For the common use case of the JWT as a bearer token, the end result is a complete authentication bypass with minimal effort.\n\n",
  "recommendation": "Update to version 3.0.0 or later.",
  "references": "- [Auth0 - Critical Vulnerabilities in JWT Libraries](https://auth0.com/blog/2015/03/31/critical-vulnerabilities-in-json-web-token-libraries/)\n- [Commit #585d0e1](https://github.com/brianloveswords/node-jws/commit/585d0e1e97b6747c10cf5b7689ccc5618a89b299#diff-4ac32a78649ca5bdd8e0ba38b7006a1e)",
  "access": "public",
  "severity": "high",
  "cwe": "CWE-310",
  "metadata": {
    "module_type": "Multi.Library",
    "exploitability": 7,
    "affected_components": ""
  },
  "url": "https://npmjs.com/advisories/88"
}
```

# Audit Level

By default, the audit will catch and fail for any vulnerability, but usually we may interested only in 
high or critical vulnerabiliities, alteast for pipelines. In such case we can give the optional flag 
'--audit-level=high', so that all vulnerabilities with criticality high and above(critical) would be 
caught. However there wouldn't be any difference in the output, the exit code would only vary, and 
depends on high / critical vulnerabilities.
```
$ npm audit --audit-level=high
--TRUNCATED--
found 25 vulnerabilities (3 low, 10 moderate, 9 high, 3 critical) in 2005 scanned packages
--TRUNCATED--

$ echo $?
1
```
The exit code is still 1, as although low and moderate vulnerabilities are ignored, there are still 9 
high and 3 critical vulnerabilites.

# Fix

In certain cases, its possible to give an automatic fix using npm with `npm audit fix` command fix 
vulnerabilities. Its not possible always though as in our case, we can simulate this with the 
--dry-run flag to foresee what really happens.
```
networkandcode@ubuntu20:~/juice-shop$ npm audit fix --dry-run
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@^2.1.2 (node_modules/jest-haste-map/node_modules/fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@2.3.2: wanted {"os":"darwin","arch":"any"} (current: {"os":"linux","arch":"x64"})

up to date in 12.151s

117 packages are looking for funding
  run `npm fund` for details

fixed 0 of 25 vulnerabilities in 2005 scanned packages
  6 vulnerabilities required manual review and could not be updated
  3 package updates for 19 vulnerabilities involved breaking changes
  (use `npm audit fix --force` to install breaking changes; or refer to `npm audit` for steps to fix these manually)
```

So it clearly says no vulnerabilities are fixed, and could also lead to breaking changes if the fix is 
forced. We have to then go through the recommendation for each vulnerability and try and fix it 
manually after reviewing that it doesnt break other packages.

Thats the end of this post, we saw how to perform few commands in the npm audit family, and how the exit
 code can be checked to see if failed auditing or not.

--end-of-post--
