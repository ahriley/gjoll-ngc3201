SELECT source_id, ra, dec, pmra, pmra_error, pmdec, pmdec_error, parallax, parallax_error, phot_g_mean_mag AS g, bp_rp, astrometric_excess_noise, astrometric_chi2_al, astrometric_n_good_obs_al, phot_bp_rp_excess_factor
FROM gaiadr2.gaia_source
WHERE ra > 160 AND ra < 195
AND dec > 40 AND dec < 70
AND pmra > -1 AND pmra < 2
AND pmdec > -2 AND pmdec < 0
AND parallax > -1 AND parallax < 1
AND bp_rp > -1 AND bp_rp < 2
AND phot_g_mean_mag <= 15
