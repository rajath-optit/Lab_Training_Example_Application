package edu.pes.recipes.controller;

import java.util.List;

import jakarta.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.Errors;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import edu.pes.recipes.model.Recipe;
import edu.pes.recipes.service.RecipeServiceInterface;

@Controller
@RequestMapping("/recipes")
public class RecipeController {

	@Autowired
	private RecipeServiceInterface recipeService;

	@GetMapping
	public String showRecipes(Model model) {
		List<Recipe> recipes = recipeService.findAll();
		model.addAttribute("recipes", recipes);
		return "recipes";
	}

	@GetMapping("/view/{id}")
	public String viewRecipe(Model model, @PathVariable int id) {
		Recipe recipe = recipeService.findById(id);
		model.addAttribute("recipe", recipe);
		return "view-recipe";
	}

	@GetMapping("/new")
	public String showNewRecipeForm(Recipe recipe) {
		return "new-recipe";
	}

	@GetMapping("/edit/{id}")
	public String showEditRecipeForm(Model model, @PathVariable int id) {
		Recipe recipe = recipeService.findById(id);
		model.addAttribute("recipe", recipe);
		return "edit-recipe";
	}

	@PostMapping("/new")
	public String addRecipe(@Valid Recipe recipe, Errors errors, Model model) {
		if (errors.hasErrors()) {
			return "new-recipe";
		}
		recipe = recipeService.create(recipe);
		return "redirect:/recipes/view/" + String.valueOf(recipe.getId());
	}

	@PostMapping("/edit/{id}")
	public String editRecipe(@Valid Recipe recipe, BindingResult result, Model model, @PathVariable Long id) {
		recipe.setId(id);
		recipeService.update(recipe);
		return "redirect:/recipes/view/" + String.valueOf(recipe.getId());
	}

	@GetMapping("/delete/{id}")
	public String deleteRecipe(Model model, @PathVariable int id) {
		recipeService.deleteRecipe(id);
		List<Recipe> recipes = recipeService.findAll();
		model.addAttribute("recipes", recipes);
		return "recipes";
	}

}
