SELECT source_id, ra, dec, pmra, pmra_error, pmdec, pmdec_error, parallax, parallax_error, phot_g_mean_mag AS g, bp_rp, astrometric_excess_noise, astrometric_chi2_al, astrometric_n_good_obs_al, phot_bp_rp_excess_factor
FROM gaiadr2.gaia_source
WHERE source_id IN (3200439105894310272, 3254112556278356608, 3187390548572555136, 3229373063616887936, 3188058536245928576, 2985543956292701312)
