    def get_easting_northing_flood_probability(self, easting, northing):
        """
        This function uses the KDTree method to find if points belong in circles.
        As the scikit learn KDTree function is not made for circles, here we train the 
        Tree with the input data (the points) and test/fit it with the circles as we can use
        the change the quarry radious to the radious of each circle.
        
        Get an array of flood risk probabilities from arrays of eastings and northings.
        Flood risk data is extracted from the Tool flood risk file. Locations
        not in a risk band circle return `Zero`, otherwise returns the name of the
        highest band it sits in.
        Parameters
        ----------
        easting: numpy.ndarray of floats
            OS Eastings of locations of interest
        northing: numpy.ndarray of floats
            Ordered sequence of postcodes
        Returns
        -------
       
        numpy.ndarray of strs
            numpy array of flood probability bands corresponding to input locations.
        """
       # initialise points in a format the tree understands
        XX = np.array([self.risk.X.values, self.risk.Y.values]) 
        train_val = XX.transpose(1, 0) 
        # initialise points to search in a format the tree understands
        YY = np.array([easting, northing])
        test_val = YY.T
        #Perform the KD tree binary search
        tree = KDTree(test_val, leaf_size=2)
        # the resulting array is an array of indeces: we need to return the prob of each circle at the possition of the index
        all_nn_indices = tree.query_radius(train_val, r = self.risk.radius)
        #array for zeros that is going to be the output. 
        output_a = np.zeros(len(test_val))
        #add index to a dataframe
        df_multi_col = pd.DataFrame(i for i in all_nn_indices)
        #delete duplicates so you choose the highest risk
        df_multi_col.drop_duplicates(keep = "first", inplace = True)
        df_multi_na = df_multi_col.dropna(thresh=1) 
        # join indexes with prob values
        df_mul_j = self.risk.join(df_multi_na, how = 'inner')
        #catch error if there are no pairs
        if len(df_mul_j.index) != 0:
            #loop over the coluns of the df and take the probability
            df_mul_j.iloc[:, 5] = df_mul_j.iloc[:, 5].astype(int)
            output_a[df_mul_j.iloc[:, 5]] = df_mul_j.percentage
            i = 1
            while i < (df_multi_col.shape[1]):
                df_mul_j = df_mul_j.dropna(subset=[i])
                df_mul_j.iloc[:, 5+i] = df_mul_j.iloc[:, 5+i].astype(int)
                # if output_a[df_mul_j[i]] < df_mul_j.percentage:
                output_a[df_mul_j.iloc[:, 5+i]] = df_mul_j.percentage
                i += 1
            #use dict to convert values to strings
            probs_dict_reverse = {1/10: 'High', 1/50: 'Medium', 1/100: 'Low', 1/1000: 'Very Low', 0: "Zero"}
            output_a = np.vectorize(probs_dict_reverse.get)(output_a)
            return output_a
        else:
            output_l = ["Zero" for i in range(len(easting))]
            output_l = np.array(output_l)
            return output_l
