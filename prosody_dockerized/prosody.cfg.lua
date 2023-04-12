-- Prosody XMPP Server Configuration
--
-- If it wasn't already obvious, -- starts a comment, and all
-- text after it on a line is ignored by Prosody.
--
-- The config is split into sections, a global section, and one
-- for each defined host that we serve. You can add as many host
-- sections as you like.
--
-- Lists are written { "like", "this", "one" }
-- Lists can also be of { 1, 2, 3 } numbers, etc.
-- Either commas, or semi-colons; may be used
-- as seperators.
--
-- A table is a list of values, except each value has a name. An
-- example table would be:
--
-- ssl = { key = "keyfile.key", certificate = "certificate.cert" }
--
-- Whitespace (that is tabs, spaces, line breaks) is mostly insignificant, so
-- can
-- be placed anywhere
-- that     you deem fitting.
--
-- Tip: You can check that the syntax of this file is correct when you have finished
-- by running: luac -p /etc/prosody/prosody.cfg.lua
-- If there are any errors, it will let you know what and where they are, otherwise it
-- will keep quiet.
--
-- Good luck, and happy Jabbering!

-- Global settings go in this section
-- (ie. those that apply to all hosts)

Host "*"
    c2s_interface = "0.0.0.0"
    s2s_interface = "0.0.0.0"

    -- This is a (by default, empty) list of accounts that are admins
    -- for the server. Note that you must create the accounts separately
    -- (see http://prosody.im/doc/creating_accounts for info)
    -- Example: admins = { "user1@example.com", "user2@example.net" }
    admins = { "admin@localhost" }

    -- This is the list of modules Prosody will load on startup.
    -- It looks for mod_modulename.lua in the plugins folder, so make sure that exists too.
    modules_enabled = {
            -- Generally required
                "roster"; -- Allow users to have a roster. Recommended ;)
                "saslauth"; -- Authentication for clients and servers. Recommended if you want to log in.
                "tls"; -- Add support for secure TLS on c2s/s2s connections
                "dialback"; -- s2s dialback support
                "disco"; -- Service discovery

            -- Not essential, but recommended
                "private"; -- Private XML storage (for room bookmarks, etc.)
                "vcard"; -- Allow users to set vCards

            -- Nice to have
                "legacyauth"; -- Legacy authentication. Only used by some old clients and bots.
                "version"; -- Replies to server version requests
                "uptime"; -- Report how long server has been running
                "time"; -- Let others know the time here on this server
                "ping"; -- Replies to XMPP pings with pongs
                "pep"; -- Enables users to publish their mood, activity, playing music and more
                "register"; -- Allow users to register on this server using a client and change passwords
                "presence";
                "pubsub";
                "mod_pubsub";
                -- "mod_pubsub";

            -- Required for daemonizing, and logging
                "posix"; -- POSIX functionality, sends server to background, enables syslog, etc.

            -- Other specific functionality
                "admin_adhoc"; -- Allows administration via an XMPP client that supports ad-hoc commands
                --"console"; -- telnet to port 5582 (needs console_enabled = true)
                --"bosh"; -- Enable BOSH clients, aka "Jabber over HTTP"
                --"httpserver"; -- Serve static files from a directory over HTTP
              };

    -- These modules are auto-loaded, should you
    -- for (for some mad reason) want to disable
    -- them then uncomment them below
    modules_disabled = {
            -- "presence";
            -- "message";
            -- "iq";
    };

    -- Disable account creation by default, for security
    -- For more information see http://prosody.im/doc/creating_accounts
    allow_registration = true;

    -- These are the SSL/TLS-related settings. If you don't want
    -- to use SSL/TLS, you may comment or remove this
    ssl = {
        key = "/etc/prosody/certs/CA/localhost/localhost.decrypted.key";
        certificate = "/etc/prosody/certs/CA/localhost/localhost.crt";
        }

    -- Hint: If you create a new log file or rename them, don't forget to update the
    --       logrotate config at /etc/logrotate.d/prosody
    log = {
        -- Log all error messages to prosody.err
        { levels = { min = "error" }, to = "file", filename = "/var/log/prosody/prosody.err" };
        -- Log everything of level "info" and higher (that is, all except "debug" messages)
        -- to prosody.log
        { levels = { min =  "info" }, to = "file", filename = "/var/log/prosody/prosody.log" };
    }

    pidfile = "/var/run/prosody/prosody.pid"

-- This allows clients to connect to localhost.
-- Obviously this domain cannot normally be accessed from other servers.
VirtualHost "localhost"

-- Component "pubsub_component.localhost" "pubsub"
--     component_secret = "key"
--     component_ports = { 5347 }
--     component_module = "component"
--     component_protocol = "xmpp"

-- Component "mycomponent.example.com" "component_secret_key"
--     component_secret = "my-secret-key"
--     secret = "my-secret-key"
--     component_ports = { 5347 }
--     component_interface = "0.0.0.0"

-- Component "pubsub_component.localhost" "pubsub" 
--     modules_enabled = {
--         "pubsub";
--     }
--     storage = "memory"
--     -- ...
--     -- Configure a pubsub node with open access
--     node_config = {
--         access_model = "open",
--         publish_model = "open",
--     }

-- -- Create the pubsub node
--     pubsub:create_node("mynode@pubsub_component.localhost", node_config)

-- Component "pubsub.localhost" "pubsub"
--     name = "Public PubSub Component"
--     storage = "memory"
--     access_model = "open"
--     node_defaults = {
--         access_model = "open",
--         publish_model = "open";
--     };

--     modules_enabled = {
--         "last",
--         "pep",
--     }
--     nodes = {
--         ["NewNode"] = {
--           access_model = "open"
--         }
--       }

    -- Set to false to disable PEP.
    -- pep = {
    --     publish_only = true;
    -- }

    -- Configure access permissions
    -- access = {
    --     pubsub_publisher = { "anyone" },
    --     pubsub_createroom = { "anyone" },
    --     pubsub_subscribe = { "anyone" },
    --     pubsub_retrieve = { "anyone" },
    -- }

    -- nodes = {
    --     ["node1"] = {
    --         access_model = "open",
    --         publish_model = "publishers",
    --     }
    -- }
    Component "pubsub.localhost" "pubsub"
        name = "Public PubSub Component"
        storage = "memory"
        access_model = "open"

        
        