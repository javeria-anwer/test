using Product.Data.Model;
using Product.Data.Interface;
using Product.Data.Repository;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace ProductsApi.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class ProductController : ControllerBase
    {
        private IProducts products = new ProductRepository();

        [HttpGet]
        public ActionResult<IEnumerable<Products>> GetAllProducts()
        {
            return products.GetAllProducts();
        }
        [HttpGet]
        public ActionResult<Products> GetMemberById(int id)
        {
            return products.GetProduct(id);
        }
    }
}
