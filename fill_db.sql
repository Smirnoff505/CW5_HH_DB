---
--- drop tables
---
DROP TABLE IF EXISTS employers CASCADE;
DROP TABLE IF EXISTS vacancies CASCADE;

-- Name: employers; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE employers (
    employer_id INT NOT NULL,
    employer_name VARCHAR(30) NOT NULL,
    vacancy_id INT

);

--
-- Name: vacancies; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE vacancies (
    vacancy_id SERIAL PRIMARY KEY,
    name_vacancy VARCHAR,
    salary INT,
    city VARCHAR,
    url TEXT,
    requirement TEXT,
    responsibility TEXT,
    create_date DATE
	);

--
-- Name: fk_vacancies_vacancy_id; Type: Constraint; Schema: -; Owner: -
--

ALTER TABLE ONLY employers
    ADD CONSTRAINT fk_employers_vacancy_id FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id);


--
-- PostgreSQL database dump complete