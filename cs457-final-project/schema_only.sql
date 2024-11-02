--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

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
-- Name: trigger_set_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trigger_set_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	NEW.updated_at = NOW();
	RETURN NEW;
END;
$$;


ALTER FUNCTION public.trigger_set_timestamp() OWNER TO postgres;

--
-- Name: update_last_modified_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_last_modified_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		NEW.return_time = NOW();
		RETURN NEW;
	END;$$;


ALTER FUNCTION public.update_last_modified_column() OWNER TO postgres;

--
-- Name: update_lastmodified_colummn(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_lastmodified_colummn() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		NEW.return_time = NOW();
		RETURN NEW;
	END$$;


ALTER FUNCTION public.update_lastmodified_colummn() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    book_id integer NOT NULL,
    title character varying(255) NOT NULL,
    authors character varying(765) NOT NULL,
    isbn character varying(255),
    language_code character varying(32),
    num_pages character varying(255),
    publisher character varying(255),
    issue_status boolean DEFAULT false NOT NULL
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_issue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_issue (
    issue_id integer NOT NULL,
    book_id integer NOT NULL,
    branch_id integer NOT NULL,
    added_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.book_issue OWNER TO postgres;

--
-- Name: book_issue_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.book_issue ALTER COLUMN issue_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.book_issue_issue_id_seq
    START WITH 10000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: book_test_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.book ALTER COLUMN book_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.book_test_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: issue_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issue_log (
    log_id integer NOT NULL,
    issue_id integer NOT NULL,
    issued_by integer NOT NULL,
    issued_to integer NOT NULL,
    issue_time timestamp without time zone NOT NULL,
    return_time timestamp without time zone
);


ALTER TABLE public.issue_log OWNER TO postgres;

--
-- Name: issue_log_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.issue_log ALTER COLUMN issue_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.issue_log_issue_id_seq
    START WITH 6000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: issue_log_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.issue_log ALTER COLUMN log_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.issue_log_log_id_seq
    START WITH 5000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: librarian; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.librarian (
    librarian_id integer NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    branch_id integer NOT NULL,
    employment_status boolean DEFAULT true NOT NULL
);


ALTER TABLE public.librarian OWNER TO postgres;

--
-- Name: librarian_librarian_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.librarian ALTER COLUMN librarian_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.librarian_librarian_id_seq
    START WITH 3000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: library_branch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library_branch (
    branch_id integer NOT NULL,
    branch_name character varying(255)
);


ALTER TABLE public.library_branch OWNER TO postgres;

--
-- Name: library_branch_branch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.library_branch ALTER COLUMN branch_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.library_branch_branch_id_seq
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: library_member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library_member (
    member_id integer NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    member_status boolean DEFAULT true NOT NULL
);


ALTER TABLE public.library_member OWNER TO postgres;

--
-- Name: library_member_member_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.library_member ALTER COLUMN member_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.library_member_member_id_seq
    START WITH 2000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: book_issue book_issue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_issue
    ADD CONSTRAINT book_issue_pkey PRIMARY KEY (issue_id);


--
-- Name: book book_test_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_test_pkey PRIMARY KEY (book_id);


--
-- Name: issue_log issue_log_issue_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_log
    ADD CONSTRAINT issue_log_issue_id_key UNIQUE (issue_id);


--
-- Name: issue_log issue_log_log_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_log
    ADD CONSTRAINT issue_log_log_id_key UNIQUE (log_id);


--
-- Name: issue_log issue_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_log
    ADD CONSTRAINT issue_log_pkey PRIMARY KEY (log_id);


--
-- Name: librarian librarian_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.librarian
    ADD CONSTRAINT librarian_pkey PRIMARY KEY (librarian_id);


--
-- Name: library_branch library_branch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_branch
    ADD CONSTRAINT library_branch_pkey PRIMARY KEY (branch_id);


--
-- Name: library_member library_member_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_member
    ADD CONSTRAINT library_member_pkey PRIMARY KEY (member_id);


--
-- Name: book_issue set_timestamp; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER set_timestamp BEFORE UPDATE ON public.book_issue FOR EACH ROW EXECUTE FUNCTION public.trigger_set_timestamp();


--
-- PostgreSQL database dump complete
--

