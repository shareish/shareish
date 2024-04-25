--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Debian 14.5-1.pgdg110+1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: mymap_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_item (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    location public.geography(Point,4326),
    type character varying(2) NOT NULL,
    category1 character varying(2) NOT NULL,
    category2 character varying(2) NOT NULL,
    category3 character varying(2) NOT NULL,
    user_id bigint NOT NULL,
    is_recurrent boolean NOT NULL,
    enddate timestamp with time zone,
    startdate timestamp with time zone NOT NULL,
    creationdate timestamp with time zone NOT NULL,
    visibility character varying(2) NOT NULL,
    closed_reason character varying(3) NOT NULL,
    use_coordinates boolean NOT NULL
);


ALTER TABLE public.mymap_item OWNER TO postgres;

--
-- Name: mymap_barter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_barter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_barter_id_seq OWNER TO postgres;

--
-- Name: mymap_barter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_barter_id_seq OWNED BY public.mymap_item.id;


--
-- Name: mymap_itemimage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_itemimage (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    item_id bigint NOT NULL,
    "position" integer NOT NULL
);


ALTER TABLE public.mymap_itemimage OWNER TO postgres;

--
-- Name: mymap_barterimage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_barterimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_barterimage_id_seq OWNER TO postgres;

--
-- Name: mymap_barterimage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_barterimage_id_seq OWNED BY public.mymap_itemimage.id;


--
-- Name: mymap_conversation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_conversation (
    id bigint NOT NULL,
    item_id bigint,
    lastmessagedate timestamp with time zone NOT NULL,
    max_users integer NOT NULL,
    closed_by_id bigint,
    CONSTRAINT mymap_conversation_max_users_check CHECK ((max_users >= 0))
);


ALTER TABLE public.mymap_conversation OWNER TO postgres;

--
-- Name: mymap_conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_conversation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_conversation_id_seq OWNER TO postgres;

--
-- Name: mymap_conversation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_conversation_id_seq OWNED BY public.mymap_conversation.id;


--
-- Name: mymap_conversationuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_conversationuser (
    id bigint NOT NULL,
    joining_date timestamp with time zone NOT NULL,
    updated_date timestamp with time zone NOT NULL,
    created_date timestamp with time zone NOT NULL,
    conversation_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.mymap_conversationuser OWNER TO postgres;

--
-- Name: mymap_conversationuser_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_conversationuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_conversationuser_id_seq OWNER TO postgres;

--
-- Name: mymap_conversationuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_conversationuser_id_seq OWNED BY public.mymap_conversationuser.id;


--
-- Name: mymap_itemcomment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_itemcomment (
    id bigint NOT NULL,
    content text NOT NULL,
    creationdate timestamp with time zone NOT NULL,
    item_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.mymap_itemcomment OWNER TO postgres;

--
-- Name: mymap_itemcomment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_itemcomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_itemcomment_id_seq OWNER TO postgres;

--
-- Name: mymap_itemcomment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_itemcomment_id_seq OWNED BY public.mymap_itemcomment.id;


--
-- Name: mymap_itemview; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_itemview (
    id bigint NOT NULL,
    view_date timestamp with time zone NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    item_id bigint NOT NULL,
    user_id bigint
);


ALTER TABLE public.mymap_itemview OWNER TO postgres;

--
-- Name: mymap_itemview_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_itemview_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_itemview_id_seq OWNER TO postgres;

--
-- Name: mymap_itemview_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_itemview_id_seq OWNED BY public.mymap_itemview.id;


--
-- Name: mymap_message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_message (
    id bigint NOT NULL,
    content text NOT NULL,
    conversation_id bigint,
    user_id bigint NOT NULL,
    date timestamp with time zone NOT NULL,
    seen boolean NOT NULL
);


ALTER TABLE public.mymap_message OWNER TO postgres;

--
-- Name: mymap_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_message_id_seq OWNER TO postgres;

--
-- Name: mymap_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_message_id_seq OWNED BY public.mymap_message.id;


--
-- Name: mymap_scheduledaccountdeletion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_scheduledaccountdeletion (
    id bigint NOT NULL,
    request_date timestamp with time zone NOT NULL,
    "interval" interval NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.mymap_scheduledaccountdeletion OWNER TO postgres;

--
-- Name: mymap_scheduledaccountdeletion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_scheduledaccountdeletion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_scheduledaccountdeletion_id_seq OWNER TO postgres;

--
-- Name: mymap_scheduledaccountdeletion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_scheduledaccountdeletion_id_seq OWNED BY public.mymap_scheduledaccountdeletion.id;


--
-- Name: mymap_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_token (
    id bigint NOT NULL,
    token character varying(40) NOT NULL,
    action character varying(50) NOT NULL,
    used_at timestamp with time zone,
    updated_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    user_id bigint NOT NULL,
    lifespan interval
);


ALTER TABLE public.mymap_token OWNER TO postgres;

--
-- Name: mymap_token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_token_id_seq OWNER TO postgres;

--
-- Name: mymap_token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_token_id_seq OWNED BY public.mymap_token.id;


--
-- Name: mymap_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    first_name character varying(50),
    last_name character varying(20),
    birth_date date NOT NULL,
    sign_up_date date NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    is_admin boolean NOT NULL,
    description text NOT NULL,
    facebook_url character varying(200) NOT NULL,
    homepage_url character varying(200) NOT NULL,
    instagram_url character varying(200) NOT NULL,
    ref_location public.geography(Point,4326),
    use_ref_loc boolean NOT NULL,
    dwithin_notifications smallint,
    mail_notif_freq_conversations character varying(1) NOT NULL,
    mail_notif_freq_events character varying(1) NOT NULL,
    mail_notif_freq_items character varying(1) NOT NULL,
    save_item_viewing boolean NOT NULL,
    is_disabled boolean NOT NULL,
    mail_notif_freq_osm character varying(1) NOT NULL,
    mail_notif_generalinfo boolean NOT NULL,
    mastodon_url character varying(200) NOT NULL,
    CONSTRAINT mymap_user_dwithin_notifications_check CHECK ((dwithin_notifications >= 0))
);


ALTER TABLE public.mymap_user OWNER TO postgres;

--
-- Name: mymap_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_user_id_seq OWNER TO postgres;

--
-- Name: mymap_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_user_id_seq OWNED BY public.mymap_user.id;


--
-- Name: mymap_userimage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_userimage (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.mymap_userimage OWNER TO postgres;

--
-- Name: mymap_userimage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_userimage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_userimage_id_seq OWNER TO postgres;

--
-- Name: mymap_userimage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_userimage_id_seq OWNED BY public.mymap_userimage.id;


--
-- Name: mymap_usermapextracategory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mymap_usermapextracategory (
    id bigint NOT NULL,
    category character varying(3) NOT NULL,
    selected boolean NOT NULL,
    update_date timestamp with time zone NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.mymap_usermapextracategory OWNER TO postgres;

--
-- Name: mymap_usermapextracategory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mymap_usermapextracategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mymap_usermapextracategory_id_seq OWNER TO postgres;

--
-- Name: mymap_usermapextracategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mymap_usermapextracategory_id_seq OWNED BY public.mymap_usermapextracategory.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: mymap_conversation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversation ALTER COLUMN id SET DEFAULT nextval('public.mymap_conversation_id_seq'::regclass);


--
-- Name: mymap_conversationuser id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversationuser ALTER COLUMN id SET DEFAULT nextval('public.mymap_conversationuser_id_seq'::regclass);


--
-- Name: mymap_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_item ALTER COLUMN id SET DEFAULT nextval('public.mymap_barter_id_seq'::regclass);


--
-- Name: mymap_itemcomment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemcomment ALTER COLUMN id SET DEFAULT nextval('public.mymap_itemcomment_id_seq'::regclass);


--
-- Name: mymap_itemimage id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemimage ALTER COLUMN id SET DEFAULT nextval('public.mymap_barterimage_id_seq'::regclass);


--
-- Name: mymap_itemview id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemview ALTER COLUMN id SET DEFAULT nextval('public.mymap_itemview_id_seq'::regclass);


--
-- Name: mymap_message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_message ALTER COLUMN id SET DEFAULT nextval('public.mymap_message_id_seq'::regclass);


--
-- Name: mymap_scheduledaccountdeletion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_scheduledaccountdeletion ALTER COLUMN id SET DEFAULT nextval('public.mymap_scheduledaccountdeletion_id_seq'::regclass);


--
-- Name: mymap_token id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_token ALTER COLUMN id SET DEFAULT nextval('public.mymap_token_id_seq'::regclass);


--
-- Name: mymap_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_user ALTER COLUMN id SET DEFAULT nextval('public.mymap_user_id_seq'::regclass);


--
-- Name: mymap_userimage id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_userimage ALTER COLUMN id SET DEFAULT nextval('public.mymap_userimage_id_seq'::regclass);


--
-- Name: mymap_usermapextracategory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_usermapextracategory ALTER COLUMN id SET DEFAULT nextval('public.mymap_usermapextracategory_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Token	6	add_token
22	Can change Token	6	change_token
23	Can delete Token	6	delete_token
24	Can view Token	6	view_token
25	Can add token	7	add_tokenproxy
26	Can change token	7	change_tokenproxy
27	Can delete token	7	delete_tokenproxy
28	Can view token	7	view_tokenproxy
29	Can add user	8	add_user
30	Can change user	8	change_user
31	Can delete user	8	delete_user
32	Can view user	8	view_user
33	Can add item	9	add_item
34	Can change item	9	change_item
35	Can delete item	9	delete_item
36	Can view item	9	view_item
37	Can add item image	10	add_itemimage
38	Can change item image	10	change_itemimage
39	Can delete item image	10	delete_itemimage
40	Can view item image	10	view_itemimage
41	Can add message	11	add_message
42	Can change message	11	change_message
43	Can delete message	11	delete_message
44	Can view message	11	view_message
45	Can add conversation	12	add_conversation
46	Can change conversation	12	change_conversation
47	Can delete conversation	12	delete_conversation
48	Can view conversation	12	view_conversation
49	Can add user image	13	add_userimage
50	Can change user image	13	change_userimage
51	Can delete user image	13	delete_userimage
52	Can view user image	13	view_userimage
53	Can add item comment	14	add_itemcomment
54	Can change item comment	14	change_itemcomment
55	Can delete item comment	14	delete_itemcomment
56	Can view item comment	14	view_itemcomment
57	Can add item view	15	add_itemview
58	Can change item view	15	change_itemview
59	Can delete item view	15	delete_itemview
60	Can view item view	15	view_itemview
61	Can add user map extra category	16	add_usermapextracategory
62	Can change user map extra category	16	change_usermapextracategory
63	Can delete user map extra category	16	delete_usermapextracategory
64	Can view user map extra category	16	view_usermapextracategory
65	Can add conversation user	17	add_conversationuser
66	Can change conversation user	17	change_conversationuser
67	Can delete conversation user	17	delete_conversationuser
68	Can view conversation user	17	view_conversationuser
69	Can add token	18	add_token
70	Can change token	18	change_token
71	Can delete token	18	delete_token
72	Can view token	18	view_token
73	Can add scheduled account deletion	19	add_scheduledaccountdeletion
74	Can change scheduled account deletion	19	change_scheduledaccountdeletion
75	Can delete scheduled account deletion	19	delete_scheduledaccountdeletion
76	Can view scheduled account deletion	19	view_scheduledaccountdeletion
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
93afcdb0a6a497699ea050e1fdb97cd21ef59371	2024-04-12 14:22:45.845873+00	1
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	authtoken	token
7	authtoken	tokenproxy
8	mymap	user
9	mymap	item
10	mymap	itemimage
11	mymap	message
12	mymap	conversation
13	mymap	userimage
14	mymap	itemcomment
15	mymap	itemview
16	mymap	usermapextracategory
17	mymap	conversationuser
18	mymap	token
19	mymap	scheduledaccountdeletion
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	mymap	0001_initial	2024-04-12 13:39:55.250791+00
2	contenttypes	0001_initial	2024-04-12 13:39:55.259564+00
3	admin	0001_initial	2024-04-12 13:39:55.275343+00
4	admin	0002_logentry_remove_auto_add	2024-04-12 13:39:55.280584+00
5	admin	0003_logentry_add_action_flag_choices	2024-04-12 13:39:55.285685+00
6	contenttypes	0002_remove_content_type_name	2024-04-12 13:39:55.296085+00
7	auth	0001_initial	2024-04-12 13:39:55.333919+00
8	auth	0002_alter_permission_name_max_length	2024-04-12 13:39:55.34053+00
9	auth	0003_alter_user_email_max_length	2024-04-12 13:39:55.346505+00
10	auth	0004_alter_user_username_opts	2024-04-12 13:39:55.351072+00
11	auth	0005_alter_user_last_login_null	2024-04-12 13:39:55.357409+00
12	auth	0006_require_contenttypes_0002	2024-04-12 13:39:55.359984+00
13	auth	0007_alter_validators_add_error_messages	2024-04-12 13:39:55.365193+00
14	auth	0008_alter_user_username_max_length	2024-04-12 13:39:55.370019+00
15	auth	0009_alter_user_last_name_max_length	2024-04-12 13:39:55.374756+00
16	auth	0010_alter_group_name_max_length	2024-04-12 13:39:55.383455+00
17	auth	0011_update_proxy_permissions	2024-04-12 13:39:55.391128+00
18	auth	0012_alter_user_first_name_max_length	2024-04-12 13:39:55.396801+00
19	authtoken	0001_initial	2024-04-12 13:39:55.41223+00
20	authtoken	0002_auto_20160226_1747	2024-04-12 13:39:55.428424+00
21	authtoken	0003_tokenproxy	2024-04-12 13:39:55.431842+00
22	mymap	0002_alter_barter_location	2024-04-12 13:39:55.438702+00
23	mymap	0003_alter_barter_location	2024-04-12 13:39:55.449498+00
24	mymap	0004_auto_20220426_1652	2024-04-12 13:39:55.458164+00
25	mymap	0005_auto_20220426_2031	2024-04-12 13:39:55.473035+00
26	mymap	0006_barter_in_progress	2024-04-12 13:39:55.478787+00
27	mymap	0007_auto_20220706_1254	2024-04-12 13:39:55.501391+00
28	mymap	0008_auto_20220713_1550	2024-04-12 13:39:55.541217+00
29	mymap	0009_auto_20220713_1556	2024-04-12 13:39:55.619898+00
30	mymap	0010_alter_item_item_type	2024-04-12 13:39:55.625217+00
31	mymap	0011_conversation_message	2024-04-12 13:39:55.644833+00
32	mymap	0012_auto_20220804_1513	2024-04-12 13:39:55.657365+00
33	mymap	0013_message_user	2024-04-12 13:39:55.666827+00
34	mymap	0014_auto_20220808_1147	2024-04-12 13:39:55.679365+00
35	mymap	0015_item_recurrent	2024-04-12 13:39:55.685519+00
36	mymap	0016_rename_recurrent_item_is_recurrent	2024-04-12 13:39:55.691405+00
37	mymap	0017_auto_20220809_1619	2024-04-12 13:39:55.702191+00
38	mymap	0018_alter_item_enddate	2024-04-12 13:39:55.70763+00
39	mymap	0019_auto_20220813_1756	2024-04-12 13:39:55.729153+00
40	mymap	0020_remove_item_image	2024-04-12 13:39:55.735696+00
41	mymap	0021_conversation_item	2024-04-12 13:39:55.746726+00
42	mymap	0022_conversation_slug	2024-04-12 13:39:55.752797+00
43	mymap	0023_alter_item_in_progress	2024-04-12 13:39:55.760632+00
44	mymap	0024_auto_20220818_1645	2024-04-12 13:39:55.77053+00
45	mymap	0025_alter_user_username	2024-04-12 13:39:55.777984+00
46	mymap	0026_auto_20220821_1520	2024-04-12 13:39:55.786863+00
47	mymap	0027_alter_user_username	2024-04-12 13:39:55.788452+00
48	mymap	0028_auto_20220828_1622	2024-04-12 13:39:55.799935+00
49	mymap	0029_auto_20220906_1223	2024-04-12 13:39:55.810885+00
50	mymap	0030_auto_20220921_0948	2024-04-12 13:39:55.827486+00
51	mymap	0031_auto_20220921_1253	2024-04-12 13:39:55.850492+00
52	mymap	0032_auto_20221128_1440	2024-04-12 13:39:55.867394+00
53	mymap	0033_auto_20221228_1349	2024-04-12 13:39:55.882465+00
54	mymap	0034_alter_user_ref_location	2024-04-12 13:39:55.889356+00
55	mymap	0035_auto_20230104_1215	2024-04-12 13:39:55.900753+00
56	mymap	0036_auto_20230107_1656	2024-04-12 13:39:55.916013+00
57	mymap	0037_item_hitcount	2024-04-12 13:39:55.923835+00
58	mymap	0038_remove_item_hitcount	2024-04-12 13:39:55.93265+00
59	mymap	0039_item_hitcount	2024-04-12 13:39:55.939498+00
60	mymap	0040_auto_20230112_1724	2024-04-12 13:39:55.954208+00
61	mymap	0041_auto_20230114_1646	2024-04-12 13:39:55.971089+00
62	mymap	0042_alter_item_item_type	2024-04-12 13:39:55.978283+00
63	mymap	0043_auto_20230116_1403	2024-04-12 13:39:56.023645+00
64	mymap	0044_remove_user_last_visit	2024-04-12 13:39:56.030193+00
65	mymap	0045_item_creationdate	2024-04-12 13:39:56.037195+00
66	mymap	0046_auto_20230225_0022	2024-04-12 13:39:56.05503+00
67	mymap	0047_auto_20230225_1425	2024-04-12 13:39:56.065453+00
68	mymap	0048_conversation_lastmessagedate	2024-04-12 13:39:56.071932+00
69	mymap	0049_alter_userimage_user	2024-04-12 13:39:56.08066+00
70	mymap	0050_auto_20230228_1629	2024-04-12 13:39:56.10127+00
71	mymap	0051_alter_item_item_type	2024-04-12 13:39:56.10755+00
72	mymap	0052_alter_item_creationdate	2024-04-12 13:39:56.119557+00
73	mymap	0053_auto_20230306_1835	2024-04-12 13:39:56.13454+00
74	mymap	0054_auto_20230307_1253	2024-04-12 13:39:56.176339+00
75	mymap	0055_auto_20230311_1434	2024-04-12 13:39:56.190431+00
76	mymap	0056_auto_20230316_0011	2024-04-12 13:39:56.204231+00
77	mymap	0057_auto_20230316_1405	2024-04-12 13:39:56.216095+00
78	mymap	0058_rename_item_type_item_type	2024-04-12 13:39:56.225838+00
79	mymap	0059_auto_20230323_1709	2024-04-12 13:39:56.267231+00
80	mymap	0060_conversation_starter_data	2024-04-12 13:39:56.283115+00
81	mymap	0061_conversation_remove_buyer	2024-04-12 13:39:56.298665+00
82	mymap	0062_auto_20230326_1431	2024-04-12 13:39:56.309661+00
83	mymap	0063_auto_20230328_1832	2024-04-12 13:39:56.337101+00
84	mymap	0064_alter_itemcomment_options	2024-04-12 13:39:56.345843+00
85	mymap	0065_alter_message_options	2024-04-12 13:39:56.354332+00
86	mymap	0066_auto_20230406_0050	2024-04-12 13:39:56.36121+00
87	mymap	0067_auto_20230406_0107	2024-04-12 13:39:56.389267+00
88	mymap	0068_remove_item_hitcount	2024-04-12 13:39:56.398998+00
89	mymap	0069_remove_item_in_progress	2024-04-12 13:39:56.415572+00
90	mymap	0070_auto_20230414_1517	2024-04-12 13:39:56.476026+00
91	mymap	0071_save_item_viewing	2024-04-12 13:39:56.485134+00
92	mymap	0072_invert_coords	2024-04-12 13:39:56.503877+00
93	mymap	0073_conversationuser	2024-04-12 13:39:56.553162+00
94	mymap	0074_auto_20230427_1205	2024-04-12 13:39:56.641471+00
95	mymap	0075_alter_user_ref_location	2024-04-12 13:39:56.650717+00
96	mymap	0076_alter_itemview_item	2024-04-12 13:39:56.664867+00
97	mymap	0077_conversation_is_closed	2024-04-12 13:39:56.672432+00
98	mymap	0078_item_visibility	2024-04-12 13:39:56.682417+00
99	mymap	0079_user_is_disabled	2024-04-12 13:39:56.693291+00
100	mymap	0080_token	2024-04-12 13:39:56.710802+00
101	mymap	0081_alter_token_action	2024-04-12 13:39:56.828552+00
102	mymap	0082_auto_20230505_1936	2024-04-12 13:39:56.843918+00
103	mymap	0083_scheduledaccountdeletion	2024-04-12 13:39:56.861518+00
104	mymap	0084_alter_message_user	2024-04-12 13:39:56.880798+00
105	mymap	0085_conversation_max_users	2024-04-12 13:39:56.891553+00
106	mymap	0086_alter_item_visibility	2024-04-12 13:39:56.903823+00
107	mymap	0087_item_closed_reason	2024-04-12 13:39:56.914304+00
108	mymap	0088_user_mail_notif_freq_osm	2024-04-12 13:39:56.923994+00
109	mymap	0089_user_mail_notif_generalinfo	2024-04-12 13:39:56.93451+00
110	mymap	0090_conversation_closed_by	2024-04-12 13:39:56.950003+00
111	mymap	0091_remove_conversation_is_closed	2024-04-12 13:39:56.95903+00
112	mymap	0092_item_force_coordinates_usage	2024-04-12 13:39:56.969503+00
113	mymap	0093_auto_20231113_1533	2024-04-12 13:39:56.996124+00
114	mymap	0094_user_mastodon_url	2024-04-12 13:39:57.006068+00
115	sessions	0001_initial	2024-04-12 13:39:57.017516+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: mymap_conversation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_conversation (id, item_id, lastmessagedate, max_users, closed_by_id) FROM stdin;
\.


--
-- Data for Name: mymap_conversationuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_conversationuser (id, joining_date, updated_date, created_date, conversation_id, user_id) FROM stdin;
\.


--
-- Data for Name: mymap_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_item (id, name, description, location, type, category1, category2, category3, user_id, is_recurrent, enddate, startdate, creationdate, visibility, closed_reason, use_coordinates) FROM stdin;
\.


--
-- Data for Name: mymap_itemcomment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_itemcomment (id, content, creationdate, item_id, user_id) FROM stdin;
\.


--
-- Data for Name: mymap_itemimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_itemimage (id, image, item_id, "position") FROM stdin;
\.


--
-- Data for Name: mymap_itemview; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_itemview (id, view_date, creation_date, item_id, user_id) FROM stdin;
\.


--
-- Data for Name: mymap_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_message (id, content, conversation_id, user_id, date, seen) FROM stdin;
\.


--
-- Data for Name: mymap_scheduledaccountdeletion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_scheduledaccountdeletion (id, request_date, "interval", user_id) FROM stdin;
\.


--
-- Data for Name: mymap_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_token (id, token, action, used_at, updated_at, created_at, user_id, lifespan) FROM stdin;
\.


--
-- Data for Name: mymap_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_user (id, password, last_login, first_name, last_name, birth_date, sign_up_date, email, username, is_active, is_admin, description, facebook_url, homepage_url, instagram_url, ref_location, use_ref_loc, dwithin_notifications, mail_notif_freq_conversations, mail_notif_freq_events, mail_notif_freq_items, save_item_viewing, is_disabled, mail_notif_freq_osm, mail_notif_generalinfo, mastodon_url) FROM stdin;
1	pbkdf2_sha256$260000$1crpwvyWwBWzFUWaOfnYLW$v0xrfiwENy8o07Gnz79NW360w/8gV745xLU7j16EsSw=	2024-04-12 14:22:45.839317+00	adrien	hoyoux	2024-04-12	2024-04-12	adrienhoyoux88@gmail.com	adrien543	t	f					\N	f	10	D	D	D	t	f	W	t	
\.


--
-- Data for Name: mymap_userimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_userimage (id, image, user_id) FROM stdin;
\.


--
-- Data for Name: mymap_usermapextracategory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mymap_usermapextracategory (id, category, selected, update_date, creation_date, user_id) FROM stdin;
1	BKC	t	2024-04-12 13:45:02.47627+00	2024-04-12 13:45:02.476286+00	1
2	DEF	t	2024-04-12 13:45:02.477821+00	2024-04-12 13:45:02.477837+00	1
3	DWS	t	2024-04-12 13:45:02.47869+00	2024-04-12 13:45:02.478701+00	1
4	FDB	t	2024-04-12 13:45:02.479779+00	2024-04-12 13:45:02.479789+00	1
5	FDS	t	2024-04-12 13:45:02.481749+00	2024-04-12 13:45:02.481782+00	1
6	FLF	t	2024-04-12 13:45:02.484343+00	2024-04-12 13:45:02.484377+00	1
7	FRS	t	2024-04-12 13:45:02.486369+00	2024-04-12 13:45:02.486385+00	1
8	GVB	t	2024-04-12 13:45:02.487627+00	2024-04-12 13:45:02.487643+00	1
9	SPK	t	2024-04-12 13:45:02.489055+00	2024-04-12 13:45:02.489069+00	1
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 76, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 19, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 115, true);


--
-- Name: mymap_barter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_barter_id_seq', 1, false);


--
-- Name: mymap_barterimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_barterimage_id_seq', 1, false);


--
-- Name: mymap_conversation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_conversation_id_seq', 1, false);


--
-- Name: mymap_conversationuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_conversationuser_id_seq', 1, false);


--
-- Name: mymap_itemcomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_itemcomment_id_seq', 1, false);


--
-- Name: mymap_itemview_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_itemview_id_seq', 1, false);


--
-- Name: mymap_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_message_id_seq', 1, false);


--
-- Name: mymap_scheduledaccountdeletion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_scheduledaccountdeletion_id_seq', 1, false);


--
-- Name: mymap_token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_token_id_seq', 1, false);


--
-- Name: mymap_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_user_id_seq', 1, true);


--
-- Name: mymap_userimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_userimage_id_seq', 1, false);


--
-- Name: mymap_usermapextracategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mymap_usermapextracategory_id_seq', 9, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: mymap_item mymap_barter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_item
    ADD CONSTRAINT mymap_barter_pkey PRIMARY KEY (id);


--
-- Name: mymap_itemimage mymap_barterimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemimage
    ADD CONSTRAINT mymap_barterimage_pkey PRIMARY KEY (id);


--
-- Name: mymap_conversation mymap_conversation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversation
    ADD CONSTRAINT mymap_conversation_pkey PRIMARY KEY (id);


--
-- Name: mymap_conversationuser mymap_conversationuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversationuser
    ADD CONSTRAINT mymap_conversationuser_pkey PRIMARY KEY (id);


--
-- Name: mymap_itemcomment mymap_itemcomment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemcomment
    ADD CONSTRAINT mymap_itemcomment_pkey PRIMARY KEY (id);


--
-- Name: mymap_itemview mymap_itemview_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemview
    ADD CONSTRAINT mymap_itemview_pkey PRIMARY KEY (id);


--
-- Name: mymap_message mymap_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_message
    ADD CONSTRAINT mymap_message_pkey PRIMARY KEY (id);


--
-- Name: mymap_scheduledaccountdeletion mymap_scheduledaccountdeletion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_scheduledaccountdeletion
    ADD CONSTRAINT mymap_scheduledaccountdeletion_pkey PRIMARY KEY (id);


--
-- Name: mymap_token mymap_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_token
    ADD CONSTRAINT mymap_token_pkey PRIMARY KEY (id);


--
-- Name: mymap_user mymap_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_user
    ADD CONSTRAINT mymap_user_email_key UNIQUE (email);


--
-- Name: mymap_user mymap_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_user
    ADD CONSTRAINT mymap_user_pkey PRIMARY KEY (id);


--
-- Name: mymap_userimage mymap_userimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_userimage
    ADD CONSTRAINT mymap_userimage_pkey PRIMARY KEY (id);


--
-- Name: mymap_usermapextracategory mymap_usermapextracategory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_usermapextracategory
    ADD CONSTRAINT mymap_usermapextracategory_pkey PRIMARY KEY (id);


--
-- Name: mymap_itemview unique__mymap_itemview__item_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemview
    ADD CONSTRAINT unique__mymap_itemview__item_user UNIQUE (item_id, user_id);


--
-- Name: mymap_usermapextracategory unique__mymap_usermapextracategory__user_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_usermapextracategory
    ADD CONSTRAINT unique__mymap_usermapextracategory__user_category UNIQUE (user_id, category);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: mymap_barter_location_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_barter_location_id ON public.mymap_item USING gist (location);


--
-- Name: mymap_barter_user_id_080e3145; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_barter_user_id_080e3145 ON public.mymap_item USING btree (user_id);


--
-- Name: mymap_barterimage_barter_id_a594a968; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_barterimage_barter_id_a594a968 ON public.mymap_itemimage USING btree (item_id);


--
-- Name: mymap_conversation_closed_by_id_9bc28182; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_conversation_closed_by_id_9bc28182 ON public.mymap_conversation USING btree (closed_by_id);


--
-- Name: mymap_conversation_item_id_e5d51438; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_conversation_item_id_e5d51438 ON public.mymap_conversation USING btree (item_id);


--
-- Name: mymap_conversationuser_conversation_id_6e8f57c9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_conversationuser_conversation_id_6e8f57c9 ON public.mymap_conversationuser USING btree (conversation_id);


--
-- Name: mymap_conversationuser_user_id_79521423; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_conversationuser_user_id_79521423 ON public.mymap_conversationuser USING btree (user_id);


--
-- Name: mymap_itemcomment_item_id_b7b41e31; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_itemcomment_item_id_b7b41e31 ON public.mymap_itemcomment USING btree (item_id);


--
-- Name: mymap_itemcomment_user_id_1ae389ce; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_itemcomment_user_id_1ae389ce ON public.mymap_itemcomment USING btree (user_id);


--
-- Name: mymap_itemview_item_id_782d4b6a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_itemview_item_id_782d4b6a ON public.mymap_itemview USING btree (item_id);


--
-- Name: mymap_itemview_user_id_7ade8dc8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_itemview_user_id_7ade8dc8 ON public.mymap_itemview USING btree (user_id);


--
-- Name: mymap_message_conversation_id_3829a27e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_message_conversation_id_3829a27e ON public.mymap_message USING btree (conversation_id);


--
-- Name: mymap_message_user_id_6805ef10; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_message_user_id_6805ef10 ON public.mymap_message USING btree (user_id);


--
-- Name: mymap_scheduledaccountdeletion_user_id_077a2437; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_scheduledaccountdeletion_user_id_077a2437 ON public.mymap_scheduledaccountdeletion USING btree (user_id);


--
-- Name: mymap_token_user_id_46270619; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_token_user_id_46270619 ON public.mymap_token USING btree (user_id);


--
-- Name: mymap_user_email_b768f2ba_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_user_email_b768f2ba_like ON public.mymap_user USING btree (email varchar_pattern_ops);


--
-- Name: mymap_user_ref_location_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_user_ref_location_id ON public.mymap_user USING gist (ref_location);


--
-- Name: mymap_userimage_user_id_525b9d31; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_userimage_user_id_525b9d31 ON public.mymap_userimage USING btree (user_id);


--
-- Name: mymap_usermapextracategory_user_id_c737f13a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mymap_usermapextracategory_user_id_c737f13a ON public.mymap_usermapextracategory USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_conversation mymap_conversation_closed_by_id_9bc28182_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversation
    ADD CONSTRAINT mymap_conversation_closed_by_id_9bc28182_fk_mymap_user_id FOREIGN KEY (closed_by_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_conversation mymap_conversation_item_id_e5d51438_fk_mymap_item_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversation
    ADD CONSTRAINT mymap_conversation_item_id_e5d51438_fk_mymap_item_id FOREIGN KEY (item_id) REFERENCES public.mymap_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_conversationuser mymap_conversationus_conversation_id_6e8f57c9_fk_mymap_con; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversationuser
    ADD CONSTRAINT mymap_conversationus_conversation_id_6e8f57c9_fk_mymap_con FOREIGN KEY (conversation_id) REFERENCES public.mymap_conversation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_conversationuser mymap_conversationuser_user_id_79521423_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_conversationuser
    ADD CONSTRAINT mymap_conversationuser_user_id_79521423_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_item mymap_item_user_id_3a9ae6cc_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_item
    ADD CONSTRAINT mymap_item_user_id_3a9ae6cc_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_itemcomment mymap_itemcomment_item_id_b7b41e31_fk_mymap_item_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemcomment
    ADD CONSTRAINT mymap_itemcomment_item_id_b7b41e31_fk_mymap_item_id FOREIGN KEY (item_id) REFERENCES public.mymap_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_itemcomment mymap_itemcomment_user_id_1ae389ce_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemcomment
    ADD CONSTRAINT mymap_itemcomment_user_id_1ae389ce_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_itemimage mymap_itemimage_item_id_b66cde0e_fk_mymap_item_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemimage
    ADD CONSTRAINT mymap_itemimage_item_id_b66cde0e_fk_mymap_item_id FOREIGN KEY (item_id) REFERENCES public.mymap_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_itemview mymap_itemview_item_id_782d4b6a_fk_mymap_item_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemview
    ADD CONSTRAINT mymap_itemview_item_id_782d4b6a_fk_mymap_item_id FOREIGN KEY (item_id) REFERENCES public.mymap_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_itemview mymap_itemview_user_id_7ade8dc8_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_itemview
    ADD CONSTRAINT mymap_itemview_user_id_7ade8dc8_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_message mymap_message_conversation_id_3829a27e_fk_mymap_conversation_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_message
    ADD CONSTRAINT mymap_message_conversation_id_3829a27e_fk_mymap_conversation_id FOREIGN KEY (conversation_id) REFERENCES public.mymap_conversation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_message mymap_message_user_id_6805ef10_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_message
    ADD CONSTRAINT mymap_message_user_id_6805ef10_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_scheduledaccountdeletion mymap_scheduledaccou_user_id_077a2437_fk_mymap_use; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_scheduledaccountdeletion
    ADD CONSTRAINT mymap_scheduledaccou_user_id_077a2437_fk_mymap_use FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_token mymap_token_user_id_46270619_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_token
    ADD CONSTRAINT mymap_token_user_id_46270619_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_userimage mymap_userimage_user_id_525b9d31_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_userimage
    ADD CONSTRAINT mymap_userimage_user_id_525b9d31_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mymap_usermapextracategory mymap_usermapextracategory_user_id_c737f13a_fk_mymap_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mymap_usermapextracategory
    ADD CONSTRAINT mymap_usermapextracategory_user_id_c737f13a_fk_mymap_user_id FOREIGN KEY (user_id) REFERENCES public.mymap_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

