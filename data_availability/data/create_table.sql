DROP TABLE IF EXISTS medical;
CREATE TABLE medical
(
    pat_id1	character varying(50),
    age_diag numeric (24,6),
    sex character varying(1),
    category character varying(20),
    t_stage character varying(5),
    n_stage character varying(5),
    m_stage character varying(5),
    stage_group character varying(10),
    hpv_status character varying(5),
    med_id int
);