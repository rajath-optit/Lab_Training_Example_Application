package edu.pes.recipes.service;

import java.util.List;

import edu.pes.recipes.model.Recipe;

public interface RecipeServiceInterface {
	
	public List<Recipe> findAll();
	
	public Recipe findById(int id);
	
	public Recipe update(Recipe recipe);
	
	public Recipe create(Recipe recipe);
	
	public void deleteRecipe(int id);

}
